"""Mapping of Ohanna-Agent infrastructure to Ohanna-Vision payloads."""

from typing import Any

from configuration.infrastructure import InfrastructureConfig


class VisionInfrastructureMapper:
    """Convert Agent infrastructure configuration to the Vision contract."""

    SCHEMA_VERSION = 1

    def to_payload(
        self,
        config: InfrastructureConfig,
    ) -> dict[str, Any]:
        """Build the infrastructure payload expected by Ohanna-Vision."""
        return {
            "schema_version": self.SCHEMA_VERSION,
            "infrastructure_id": config.infrastructure.id,
            "name": config.infrastructure.name,
            "environment": config.infrastructure.environment,
            "metadata": {
                "version": config.metadata.version,
                "tags": list(config.metadata.tags),
            },
            "nodes": [
                {
                    "node_id": node.id,
                    "name": node.name,
                    "description": node.description,
                    "endpoint": {
                        "type": node.endpoint.type,
                        "address": node.endpoint.address,
                    },
                }
                for node in config.nodes
            ],
            "services": [
                {
                    "service_id": service.id,
                    "name": service.name,
                    "type": service.type,
                    "node_id": service.node,
                    "port": service.port,
                }
                for service in config.services
            ],
        }