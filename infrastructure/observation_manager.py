"""Backward-compatible infrastructure observation manager."""

from infrastructure.infrastructure_health_manager import (
    InfrastructureHealthManager,
)

ObservationManager = InfrastructureHealthManager

__all__ = [
    "InfrastructureHealthManager",
    "ObservationManager",
]
