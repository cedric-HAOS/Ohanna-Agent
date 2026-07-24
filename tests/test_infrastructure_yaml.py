from pathlib import Path

import yaml


def test_real_infrastructure_yaml_declares_dns_service() -> None:
    path = Path("config/infrastructure.yaml")

    data = yaml.safe_load(path.read_text(encoding="utf-8"))

    node = data["nodes"][0]
    service = data["services"][0]

    assert node["id"] == "infra-01"
    assert node["name"] == "INFRA-01"
    assert node["endpoint"]["type"] == "ip"
    assert node["endpoint"]["address"] == "192.168.1.10"

    assert service["id"] == "dns-primary"
    assert service["name"] == "DNS principal"
    assert service["type"] == "dns"
    assert service["node"] == "infra-01"
    assert service["port"] == 53


def test_real_infrastructure_yaml_declares_complete_topology() -> None:
    path = Path("config/infrastructure.yaml")

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    topology = data["topology"]

    assert len(topology["devices"]) == 9
    assert len(topology["links"]) == 8
    assert len(topology["layouts"]) == 1

    rpi_link = next(
        device for device in topology["devices"] if device["id"] == "rpi-link"
    )

    assert rpi_link["node"] == "infra-01"

    layout = topology["layouts"][0]

    assert layout["positions"]["rpi-link"] == {
        "column": 4,
        "row": 0,
    }
