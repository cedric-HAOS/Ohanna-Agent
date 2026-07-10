"""Infrastructure observation model."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from infrastructure.enums import HealthStatus


@dataclass(slots=True)
class Observation:
    """Represents a runtime observation emitted by a plugin or checker."""

    target_name: str

    health: HealthStatus

    source: str

    message: str = ""

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    metadata: dict[str, Any] = field(default_factory=dict)