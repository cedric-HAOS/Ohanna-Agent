"""Long-running Ohana-Agent production runtime."""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass, field
from threading import Event
from time import monotonic
from typing import Any

from observer.exporters import (
    VisionClient,
    VisionClientError,
)
from scheduler import Scheduler

LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class ProductionAgent:
    """Run the configured Ohana-Agent scheduler continuously."""

    scheduler: Scheduler
    vision_client: VisionClient | None = None
    infrastructure_payload: dict[str, Any] | None = None
    tick_interval_seconds: float = 1.0
    infrastructure_retry_seconds: float = 10.0
    infrastructure_refresh_seconds: float = 300.0
    monotonic_clock: Callable[[], float] = field(
        default=monotonic,
        repr=False,
    )
    _stop_event: Event = field(
        default_factory=Event,
        init=False,
        repr=False,
    )
    _infrastructure_synchronized: bool = field(
        default=False,
        init=False,
        repr=False,
    )
    _next_infrastructure_refresh_at: float | None = field(
        default=None,
        init=False,
        repr=False,
    )

    def __post_init__(self) -> None:
        """Validate runtime settings."""
        if self.tick_interval_seconds <= 0:
            raise ValueError("tick_interval_seconds must be greater than zero.")

        if self.infrastructure_retry_seconds <= 0:
            raise ValueError("infrastructure_retry_seconds must be greater than zero.")

        if self.infrastructure_refresh_seconds <= 0:
            raise ValueError(
                "infrastructure_refresh_seconds must be greater than zero."
            )

        client_is_configured = self.vision_client is not None
        payload_is_configured = self.infrastructure_payload is not None

        if client_is_configured != payload_is_configured:
            raise ValueError(
                "vision_client and infrastructure_payload must be configured together."
            )

    @property
    def running(self) -> bool:
        """Return whether the production agent is running."""
        return (
            self.scheduler.running
            and self._infrastructure_synchronized
            and not self._stop_event.is_set()
        )

    @property
    def infrastructure_synchronized(self) -> bool:
        """Return whether Vision accepted the infrastructure snapshot."""
        return self._infrastructure_synchronized

    def start(self) -> None:
        """Synchronize Vision and start the scheduler when possible."""
        if self.scheduler.running:
            return

        self._stop_event.clear()

        if not self._synchronize_infrastructure():
            return

        self._start_scheduler()

    def tick(self) -> None:
        """Execute one scheduler iteration."""
        results = self.scheduler.tick()

        for result in results:
            if result.success:
                LOGGER.info(
                    "Scheduled task completed: %s",
                    result.command,
                )
            else:
                LOGGER.error(
                    "Scheduled task failed: %s — %s",
                    result.command,
                    result.error or "unknown error",
                )

    def run(self) -> None:
        """Run until a stop request is received."""
        self._stop_event.clear()

        try:
            while not self._stop_event.is_set():
                if not self._infrastructure_synchronized:
                    if not self._synchronize_infrastructure():
                        if self._stop_event.wait(self.infrastructure_retry_seconds):
                            break

                        continue

                if not self.scheduler.running:
                    self._start_scheduler()

                if self._stop_event.wait(self.tick_interval_seconds):
                    break

                if self._infrastructure_refresh_due():
                    if not self._synchronize_infrastructure():
                        if self._stop_event.wait(self.infrastructure_retry_seconds):
                            break

                        continue

                self.tick()
        finally:
            self.stop()

    def request_stop(self) -> None:
        """Request a graceful shutdown."""
        LOGGER.info("Ohana-Agent shutdown requested.")
        self._stop_event.set()

    def stop(self) -> None:
        """Stop the scheduler."""
        if self.scheduler.running:
            self.scheduler.stop()

        self._infrastructure_synchronized = False
        self._next_infrastructure_refresh_at = None
        self._stop_event.set()
        LOGGER.info("Ohana-Agent stopped.")

    def _start_scheduler(self) -> None:
        """Start observations after infrastructure synchronization."""
        self.scheduler.start()
        LOGGER.info("Ohana-Agent started.")

    def _synchronize_infrastructure(self) -> bool:
        """Send the complete infrastructure snapshot to Vision."""
        if self.vision_client is None:
            self._infrastructure_synchronized = True
            self._next_infrastructure_refresh_at = None
            return True

        if self.infrastructure_payload is None:
            raise RuntimeError(
                "Infrastructure payload is missing while "
                "Vision synchronization is enabled."
            )

        try:
            self.vision_client.send_infrastructure(self.infrastructure_payload)
        except VisionClientError as error:
            if self.scheduler.running:
                self.scheduler.stop()

            self._infrastructure_synchronized = False
            self._next_infrastructure_refresh_at = None

            LOGGER.warning(
                "Unable to synchronize infrastructure with Ohana-Vision: %s",
                error,
            )
            return False

        self._infrastructure_synchronized = True
        self._next_infrastructure_refresh_at = (
            self.monotonic_clock() + self.infrastructure_refresh_seconds
        )

        LOGGER.info("Infrastructure synchronized with Ohana-Vision.")
        return True

    def _infrastructure_refresh_due(self) -> bool:
        """Return whether the infrastructure snapshot must be refreshed."""
        if self._next_infrastructure_refresh_at is None:
            return False

        return self.monotonic_clock() >= self._next_infrastructure_refresh_at
