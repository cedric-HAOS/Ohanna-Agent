# tests/test_infrastructure_yaml_example.py

from pathlib import Path

import yaml


def test_infrastructure_example_yaml_exists() -> None:
    path = Path("config/infrastructure.example.yaml")

    assert path.exists()


def test_infrastructure_example_yaml_has_expected_root_sections() -> None:
    path = Path("config/infrastructure.example.yaml")

    data = yaml.safe_load(path.read_text(encoding="utf-8"))

    assert "infrastructure" in data
    assert "metadata" in data
    assert "nodes" in data
    assert "services" in data


def test_infrastructure_example_yaml_declares_infrastructure_identity() -> None:
    path = Path("config/infrastructure.example.yaml")

    data = yaml.safe_load(path.read_text(encoding="utf-8"))

    assert data["infrastructure"]["id"] == "ohanna-house"
    assert data["infrastructure"]["name"] == "Ohanna House"
    assert data["infrastructure"]["environment"] == "production"


def test_infrastructure_example_yaml_declares_nodes() -> None:
    path = Path("config/infrastructure.example.yaml")

    data = yaml.safe_load(path.read_text(encoding="utf-8"))

    nodes = data["nodes"]

    assert len(nodes) == 2
    assert nodes[0]["endpoint"]["type"] == "ip"
    assert nodes[0]["endpoint"]["address"] == "192.168.1.54"


def test_infrastructure_example_yaml_declares_services() -> None:
    path = Path("config/infrastructure.example.yaml")

    data = yaml.safe_load(path.read_text(encoding="utf-8"))

    services = data["services"]

    assert len(services) == 2
    assert services[0]["id"] == "dns-primary"
    assert services[0]["type"] == "dns"
    assert services[0]["node"] == "infra-01"


def test_infrastructure_example_yaml_declares_service_endpoints() -> None:
    path = Path("config/infrastructure.example.yaml")

    data = yaml.safe_load(path.read_text(encoding="utf-8"))

    dns_service = data["services"][0]

    assert dns_service["port"] == 53
