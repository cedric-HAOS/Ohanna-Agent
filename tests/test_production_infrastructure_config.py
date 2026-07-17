from pathlib import Path

from loader import InfrastructureLoader


def test_production_infrastructure_declares_infra_01() -> None:
    config = InfrastructureLoader().load(Path("config/infrastructure.yaml"))

    assert len(config.nodes) == 1

    node = config.nodes[0]

    assert node.id == "infra-01"
    assert node.endpoint.address == "192.168.1.10"


def test_production_infrastructure_declares_primary_dns() -> None:
    config = InfrastructureLoader().load(Path("config/infrastructure.yaml"))

    assert len(config.services) == 1

    service = config.services[0]

    assert service.id == "dns-primary"
    assert service.type == "dns"
    assert service.node == "infra-01"
    assert service.port == 53
