"""Declarative DNS plugin configuration models."""

from pydantic import Field, field_validator

from configuration.base import Config


class DNSPolicyConfig(Config):
    """Policy used to evaluate the DNS capability."""

    minimum_healthy_servers: int = 1


class DNSPluginConfig(Config):
    """Declarative configuration for the DNS plugin."""

    services: list[str] = Field(default_factory=list)
    queries: list[str] = Field(default_factory=list)
    timeout: float = 2.0
    retries: int = 1
    policy: DNSPolicyConfig = Field(
        default_factory=DNSPolicyConfig
    )

    @field_validator("services")
    @classmethod
    def validate_services(
        cls,
        services: list[str],
    ) -> list[str]:
        """Reject empty infrastructure service identifiers."""
        normalized_services = [
            service.strip()
            for service in services
        ]

        if any(not service for service in normalized_services):
            raise ValueError(
                "DNS service identifiers must not be empty."
            )

        return normalized_services

    @field_validator("queries")
    @classmethod
    def validate_queries(
        cls,
        queries: list[str],
    ) -> list[str]:
        """Reject empty DNS queries."""
        normalized_queries = [
            query.strip()
            for query in queries
        ]

        if any(not query for query in normalized_queries):
            raise ValueError(
                "DNS queries must not be empty."
            )

        return normalized_queries