"""Build DNS runtime configuration from declarative configuration."""

from configuration.dns import DNSPluginConfig
from infrastructure import Infrastructure, ServiceType
from plugins.dns.dns_config import (
    DNSConfig,
    DNSPolicyConfig,
    DNSServerConfig,
)


class DNSConfigurationBuilder:
    """Build DNS plugin configuration from infrastructure services."""

    def build(
        self,
        infrastructure: Infrastructure,
        config: DNSPluginConfig,
    ) -> DNSConfig:
        """Build a DNSConfig ready to be used by DNSPlugin."""
        servers = [
            self._build_server(
                infrastructure,
                service_id,
            )
            for service_id in config.services
        ]

        return DNSConfig(
            servers=servers,
            queries=config.queries.copy(),
            timeout=config.timeout,
            retries=config.retries,
            policy=DNSPolicyConfig(
                minimum_healthy_servers=(config.policy.minimum_healthy_servers),
            ),
        )

    def _build_server(
        self,
        infrastructure: Infrastructure,
        service_id: str,
    ) -> DNSServerConfig:
        """Resolve one DNS service from the infrastructure."""
        service = self._find_service(
            infrastructure,
            service_id,
        )

        if service is None:
            raise LookupError(f"Infrastructure service not found: {service_id!r}.")

        if service.type is not ServiceType.DNS:
            raise ValueError(
                f"Infrastructure service {service_id!r} is not a DNS service."
            )

        if service.endpoint is None:
            raise LookupError(f"DNS service {service_id!r} has no endpoint.")

        return DNSServerConfig(
            name=service.name,
            address=service.endpoint.address,
            enabled=(service.enabled and service.endpoint.enabled),
        )

    @staticmethod
    def _find_service(
        infrastructure: Infrastructure,
        service_id: str,
    ):
        """Return an infrastructure service by its stable identifier."""
        for node in infrastructure.nodes:
            for service in node.services:
                if service.name == service_id:
                    return service

        return None
