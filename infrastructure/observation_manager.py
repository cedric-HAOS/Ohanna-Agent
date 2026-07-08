"""Infrastructure observation manager."""

from dataclasses import dataclass, field

from infrastructure.enums import ServiceType
from infrastructure.observation import Observation
from infrastructure.runtime import InfrastructureRuntime


@dataclass(slots=True)
class ObservationManager:
    """Applies observations to infrastructure runtime objects."""

    runtime: InfrastructureRuntime
    observations: list[Observation] = field(default_factory=list)

    def record(self, observation: Observation) -> bool:
        """Record an observation and apply it to a matching runtime target."""
        self.observations.append(observation)

        if self._apply_to_service(observation):
            return True

        if self._apply_to_node(observation):
            return True

        return False

    def _apply_to_service(self, observation: Observation) -> bool:
        """Apply an observation to a matching service runtime."""
        try:
            service_type = ServiceType(observation.target_name)
        except ValueError:
            return False

        service_runtime = self.runtime.get_service_runtime_by_type(service_type)
        if service_runtime is None:
            return False

        service_runtime.update_health(observation.health)
        return True

    def _apply_to_node(self, observation: Observation) -> bool:
        """Apply an observation to a matching node runtime."""
        node_runtime = self.runtime.get_node_runtime_by_name(observation.target_name)
        if node_runtime is None:
            return False

        node_runtime.update_health(observation.health)
        return True