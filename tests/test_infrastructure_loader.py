from pathlib import Path

from loader import InfrastructureLoader


def test_loader_returns_infrastructure_config() -> None:
    loader = InfrastructureLoader()

    config = loader.load(Path("config/infrastructure.example.yaml"))

    assert config.infrastructure.id == "ohanna-house"


def test_loader_loads_nodes() -> None:
    loader = InfrastructureLoader()

    config = loader.load("config/infrastructure.example.yaml")

    assert len(config.nodes) == 2

    assert config.nodes[0].id == "infra-01"


def test_loader_loads_services() -> None:
    loader = InfrastructureLoader()

    config = loader.load("config/infrastructure.example.yaml")

    assert len(config.services) == 2

    assert config.services[0].id == "dns-primary"


def test_loader_loads_endpoints() -> None:
    loader = InfrastructureLoader()

    config = loader.load("config/infrastructure.example.yaml")

    assert config.services[0].port == 53


def test_loader_accepts_path_object() -> None:
    loader = InfrastructureLoader()

    config = loader.load(Path("config/infrastructure.example.yaml"))

    assert config.infrastructure.name == "Ohanna House"
