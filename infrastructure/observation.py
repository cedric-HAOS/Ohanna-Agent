"""Backward-compatible infrastructure observation import."""

from infrastructure.infrastructure_health_update import (
    InfrastructureHealthUpdate,
)

Observation = InfrastructureHealthUpdate

__all__ = [
    "InfrastructureHealthUpdate",
    "Observation",
]
