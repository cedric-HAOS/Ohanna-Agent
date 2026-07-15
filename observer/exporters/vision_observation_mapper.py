"""Mapping of Ohanna-Agent observations to Ohanna-Vision payloads."""

from typing import Any

from observer.observation import Observation
from observer.observation_status import ObservationStatus


class VisionObservationMapper:
    """Convert Agent observations to the Ohanna-Vision REST contract."""

    _STATUS_MAPPING = {
        ObservationStatus.HEALTHY: "healthy",
        ObservationStatus.DEGRADED: "degraded",
        ObservationStatus.UNHEALTHY: "unavailable",
        ObservationStatus.UNKNOWN: "unknown",
    }

    def to_payload(
        self,
        observation: Observation,
    ) -> dict[str, Any]:
        """Build the payload expected by Ohanna-Vision."""
        metadata = observation.metadata.copy()

        metadata["agent_observation"] = {
            "id": str(observation.id),
            "source": observation.source,
            "success": observation.success,
            "message": observation.message,
        }

        return {
            "capability_id": observation.capability,
            "service_id": observation.service,
            "node_id": observation.node,
            "status": self._STATUS_MAPPING[observation.status],
            "observed_at": observation.timestamp.isoformat(),
            "latency_ms": observation.latency_ms,
            "metadata": metadata,
        }