from configuration.infrastructure import (
    InfrastructureConfig,
    InfrastructureIdentityConfig,
    InfrastructureMetadataConfig,
    NodeConfig,
    NodeEndpointConfig,
    ServiceConfig,
)
from observer.exporters import VisionInfrastructureMapper


def build_infrastructure_config() -> InfrastructureConfig:
    """Build a stable infrastructure configuration used by mapper tests."""
    return InfrastructureConfig(
        infrastructure=InfrastructureIdentityConfig(
            id="ohanna-house",
            name="Ohanna House",
            environment="production",
        ),
        metadata=InfrastructureMetadataConfig(
            version="1.0",
            tags=[
                "production",
                "home",
            ],
        ),
        nodes=[
            NodeConfig(
                id="infra-01",
                name="INFRA-01",
                description=(
                    "Serveur principal de l'infrastructure Ohanna"
                ),
                endpoint=NodeEndpointConfig(
                    type="ip",
                    address="192.168.1.10",
                ),
            ),
            NodeConfig(
                id="ha-green",
                name="HA-Green",
                description="Instance Home Assistant principale",
                endpoint=NodeEndpointConfig(
                    type="ip",
                    address="192.168.1.20",
                ),
            ),
        ],
        services=[
            ServiceConfig(
                id="dns-primary",
                name="DNS principal",
                type="dns",
                node="infra-01",
                port=53,
            ),
            ServiceConfig(
                id="mqtt-primary",
                name="MQTT principal",
                type="mqtt",
                node="ha-green",
                port=1883,
            ),
        ],
    )


def test_mapper_builds_vision_infrastructure_payload() -> None:
    mapper = VisionInfrastructureMapper()

    payload = mapper.to_payload(
        build_infrastructure_config(),
    )

    assert payload == {
        "schema_version": 1,
        "infrastructure_id": "ohanna-house",
        "name": "Ohanna House",
        "environment": "production",
        "metadata": {
            "version": "1.0",
            "tags": [
                "production",
                "home",
            ],
        },
        "nodes": [
            {
                "node_id": "infra-01",
                "name": "INFRA-01",
                "description": (
                    "Serveur principal de l'infrastructure Ohanna"
                ),
                "endpoint": {
                    "type": "ip",
                    "address": "192.168.1.10",
                },
            },
            {
                "node_id": "ha-green",
                "name": "HA-Green",
                "description": (
                    "Instance Home Assistant principale"
                ),
                "endpoint": {
                    "type": "ip",
                    "address": "192.168.1.20",
                },
            },
        ],
        "services": [
            {
                "service_id": "dns-primary",
                "name": "DNS principal",
                "type": "dns",
                "node_id": "infra-01",
                "port": 53,
            },
            {
                "service_id": "mqtt-primary",
                "name": "MQTT principal",
                "type": "mqtt",
                "node_id": "ha-green",
                "port": 1883,
            },
        ],
    }


def test_mapper_supports_empty_infrastructure() -> None:
    config = InfrastructureConfig(
        infrastructure=InfrastructureIdentityConfig(
            id="empty",
            name="Empty infrastructure",
        ),
    )

    payload = VisionInfrastructureMapper().to_payload(config)

    assert payload["nodes"] == []
    assert payload["services"] == []


def test_mapper_preserves_service_without_port() -> None:
    config = InfrastructureConfig(
        infrastructure=InfrastructureIdentityConfig(
            id="ohanna-house",
            name="Ohanna House",
        ),
        nodes=[
            NodeConfig(
                id="infra-01",
                name="INFRA-01",
                endpoint=NodeEndpointConfig(
                    type="ip",
                    address="192.168.1.10",
                ),
            ),
        ],
        services=[
            ServiceConfig(
                id="service-without-port",
                name="Service sans port",
                type="other",
                node="infra-01",
            ),
        ],
    )

    payload = VisionInfrastructureMapper().to_payload(config)

    assert payload["services"][0]["port"] is None


def test_mapper_does_not_share_metadata_tags() -> None:
    config = build_infrastructure_config()

    payload = VisionInfrastructureMapper().to_payload(config)

    payload["metadata"]["tags"].append("modified")

    assert config.metadata.tags == [
        "production",
        "home",
    ]


def test_mapper_only_emits_public_contract_fields() -> None:
    payload = VisionInfrastructureMapper().to_payload(
        build_infrastructure_config(),
    )

    assert set(payload) == {
        "schema_version",
        "infrastructure_id",
        "name",
        "environment",
        "metadata",
        "nodes",
        "services",
    }

    assert set(payload["nodes"][0]) == {
        "node_id",
        "name",
        "description",
        "endpoint",
    }

    assert set(payload["services"][0]) == {
        "service_id",
        "name",
        "type",
        "node_id",
        "port",
    }