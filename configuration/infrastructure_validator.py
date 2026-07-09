# configuration/infrastructure_validator.py

from ipaddress import ip_address

from configuration.infrastructure import InfrastructureConfig


class InfrastructureValidationError(ValueError):
    """Raised when an infrastructure configuration is invalid."""


class InfrastructureValidator:
    """Validates an infrastructure configuration."""

    def validate(self, config: InfrastructureConfig) -> None:
        """Validate an infrastructure configuration."""

        self._validate_node_ids_are_unique(config)
        self._validate_service_ids_are_unique(config)
        self._validate_node_addresses(config)
        self._validate_service_nodes_exist(config)
        self._validate_service_ports(config)

    def _validate_node_ids_are_unique(
        self,
        config: InfrastructureConfig,
    ) -> None:
        node_ids = [node.id for node in config.nodes]

        if len(node_ids) != len(set(node_ids)):
            raise InfrastructureValidationError("Node identifiers must be unique.")

    def _validate_service_ids_are_unique(
        self,
        config: InfrastructureConfig,
    ) -> None:
        service_ids = [service.id for service in config.services]

        if len(service_ids) != len(set(service_ids)):
            raise InfrastructureValidationError("Service identifiers must be unique.")

    def _validate_node_addresses(
        self,
        config: InfrastructureConfig,
    ) -> None:
        for node in config.nodes:
            if node.endpoint.type != "ip":
                raise InfrastructureValidationError(
                    f"Unsupported endpoint type: {node.endpoint.type}"
                )

            try:
                ip_address(node.endpoint.address)
            except ValueError as exc:
                raise InfrastructureValidationError(
                    f"Invalid IP address: {node.endpoint.address}"
                ) from exc

    def _validate_service_nodes_exist(
        self,
        config: InfrastructureConfig,
    ) -> None:
        node_ids = {node.id for node in config.nodes}

        for service in config.services:
            if service.node not in node_ids:
                raise InfrastructureValidationError(
                    f"Service '{service.id}' references unknown node '{service.node}'."
                )
    
    def _validate_service_ports(
        self,
        config: InfrastructureConfig,
    ) -> None:
        for service in config.services:
            if service.port is None:
                continue

            if service.port < 1 or service.port > 65535:
                raise InfrastructureValidationError(
                    f"Invalid port '{service.port}' for service '{service.id}'."
                )