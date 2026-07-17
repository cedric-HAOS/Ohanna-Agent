"""Long-running Ohanna-Agent production runtime."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from threading import Event

from scheduler import Scheduler

LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class ProductionAgent:
    """Run the configured Ohanna-Agent scheduler continuously."""

    scheduler: Scheduler
    tick_interval_seconds: float = 1.0
    _stop_event: Event = field(
        default_factory=Event,
        init=False,
        repr=False,
    )

    def __post_init__(self) -> None:
        """Validate runtime settings."""
        if self.tick_interval_seconds <= 0:
            raise ValueError("tick_interval_seconds must be greater than zero.")

    @property
    def running(self) -> bool:
        """Return whether the production agent is running."""
        return self.scheduler.running and not self._stop_event.is_set()

    def start(self) -> None:
        """Start the scheduler."""
        if self.scheduler.running:
            return

        self._stop_event.clear()
        self.scheduler.start()
        LOGGER.info("Ohanna-Agent started.")

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
        self.start()

        try:
            while not self._stop_event.wait(self.tick_interval_seconds):
                self.tick()
        finally:
            self.stop()

    def request_stop(self) -> None:
        """Request a graceful shutdown."""
        LOGGER.info("Ohanna-Agent shutdown requested.")
        self._stop_event.set()

    def stop(self) -> None:
        """Stop the scheduler."""
        if self.scheduler.running:
            self.scheduler.stop()

        self._stop_event.set()
        LOGGER.info("Ohanna-Agent stopped.")
