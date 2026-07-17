from enum import StrEnum


class ObservationStatus(StrEnum):
    """Standard status for an observation result."""

    UNKNOWN = "unknown"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
