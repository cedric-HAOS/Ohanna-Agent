from builder import InfrastructureBuilder
from infrastructure.enums import EndpointType, ServiceType
from loader import InfrastructureLoader


def build_infrastructure():
    loader = InfrastructureLoader()
    builder = InfrastructureBuilder()

    config = loader.load("config/infrastructure.example.yaml")

    return builder.build(config)


def test_builder_builds_infrastructure() -> None:
    infrastructure = build_infrastructure()

    assert infrastructure.name == "Ohana House"


def test_builder_builds_nodes() -> None:
    infrastructure = build_infrastructure()

    assert len(infrastructure.nodes) == 2
    assert infrastructure.nodes[0].name == "infra-01"


def test_builder_builds_node_endpoints() -> None:
    infrastructure = build_infrastructure()

    node = infrastructure.nodes[0]

    assert len(node.endpoints) == 1
    assert node.endpoints[0].type == EndpointType.IP
    assert node.endpoints[0].address == "192.168.1.10"


def test_builder_builds_services() -> None:
    infrastructure = build_infrastructure()

    node = infrastructure.nodes[0]

    assert len(node.services) == 1
    assert node.services[0].name == "dns-primary"
    assert node.services[0].type == ServiceType.DNS


def test_builder_builds_service_endpoint() -> None:
    infrastructure = build_infrastructure()

    service = infrastructure.nodes[0].services[0]

    assert service.endpoint is not None
    assert service.endpoint.type == EndpointType.IP
    assert service.endpoint.address == "192.168.1.10"
    assert service.endpoint.port == 53
