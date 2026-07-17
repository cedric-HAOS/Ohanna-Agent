import pytest

from configuration.infrastructure import (
    InfrastructureConfig,
    InfrastructureIdentityConfig,
    NodeConfig,
    NodeEndpointConfig,
    ServiceConfig,
)
from configuration.infrastructure_validator import (
    InfrastructureValidationError,
    InfrastructureValidator,
)


def build_valid_config() -> InfrastructureConfig:
    return InfrastructureConfig(
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
                    address="192.168.1.54",
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
        ],
    )


def test_validator_accepts_valid_config() -> None:
    InfrastructureValidator().validate(build_valid_config())


def test_validator_rejects_duplicate_node_ids() -> None:
    config = InfrastructureConfig(
        infrastructure=InfrastructureIdentityConfig(
            id="ohanna-house",
            name="Ohanna House",
        ),
        nodes=[
            NodeConfig(
                id="infra-01",
                name="INFRA-01",
                endpoint=NodeEndpointConfig(type="ip", address="192.168.1.54"),
            ),
            NodeConfig(
                id="infra-01",
                name="Duplicate",
                endpoint=NodeEndpointConfig(type="ip", address="192.168.1.55"),
            ),
        ],
    )

    with pytest.raises(InfrastructureValidationError):
        InfrastructureValidator().validate(config)


def test_validator_rejects_duplicate_service_ids() -> None:
    config = build_valid_config()
    config.services.append(
        ServiceConfig(
            id="dns-primary",
            name="DNS duplicate",
            type="dns",
            node="infra-01",
            port=54,
        )
    )

    with pytest.raises(InfrastructureValidationError):
        InfrastructureValidator().validate(config)


def test_validator_rejects_invalid_node_endpoint_type() -> None:
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
                    type="tcp",
                    address="192.168.1.54",
                ),
            ),
        ],
    )

    with pytest.raises(InfrastructureValidationError):
        InfrastructureValidator().validate(config)


def test_validator_rejects_invalid_node_address() -> None:
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
                    address="not-an-ip",
                ),
            ),
        ],
    )

    with pytest.raises(InfrastructureValidationError):
        InfrastructureValidator().validate(config)


def test_validator_rejects_service_referencing_unknown_node() -> None:
    config = InfrastructureConfig(
        infrastructure=InfrastructureIdentityConfig(
            id="ohanna-house",
            name="Ohanna House",
        ),
        nodes=[
            NodeConfig(
                id="infra-01",
                name="INFRA-01",
                endpoint=NodeEndpointConfig(type="ip", address="192.168.1.54"),
            ),
        ],
        services=[
            ServiceConfig(
                id="dns-primary",
                name="DNS principal",
                type="dns",
                node="unknown-node",
                port=53,
            ),
        ],
    )

    with pytest.raises(InfrastructureValidationError):
        InfrastructureValidator().validate(config)


def test_validator_rejects_port_below_range() -> None:
    config = build_valid_config()
    config.services.append(
        ServiceConfig(
            id="bad-service",
            name="Bad service",
            type="dns",
            node="infra-01",
            port=0,
        )
    )

    with pytest.raises(InfrastructureValidationError):
        InfrastructureValidator().validate(config)


def test_validator_rejects_port_above_range() -> None:
    config = build_valid_config()
    config.services.append(
        ServiceConfig(
            id="bad-service",
            name="Bad service",
            type="dns",
            node="infra-01",
            port=65536,
        )
    )

    with pytest.raises(InfrastructureValidationError):
        InfrastructureValidator().validate(config)
