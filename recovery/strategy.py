"""Recovery strategies for Ohanna-Agent."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol

from health.monitor import HealthResult, HealthStatus
from recovery.action import RecoveryAction
from recovery.result import RecoveryResult


class RecoveryStrategy(Protocol):
    """Protocol implemented by recovery strategies."""

    def can_handle(self, result: HealthResult) -> bool:
        """Return whether this strategy can handle the health result."""
        ...

    def execute(self, result: HealthResult) -> RecoveryResult:
        """Execute the recovery strategy."""
        ...


class StaticRecoveryStrategy:
    """Simple strategy executing a predefined recovery action."""

    def __init__(
        self,
        source: str,
        action: RecoveryAction,
        statuses: Iterable[HealthStatus] | None = None,
    ) -> None:
        self.source = source
        self.action = action
        self.statuses = set(statuses or {HealthStatus.DEGRADED, HealthStatus.UNHEALTHY})

    def can_handle(self, result: HealthResult) -> bool:
        """Return whether this strategy can handle the health result."""
        return result.name == self.source and result.status in self.statuses

    def execute(self, result: HealthResult) -> RecoveryResult:
        """Execute the configured action."""
        return self.action.execute()