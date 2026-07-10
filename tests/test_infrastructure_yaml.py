from pathlib import Path

import yaml


def test_real_infrastructure_yaml_declares_dns_service() -> None:
    path = Path("config/infrastructure.yaml")

    data = yaml.safe_load(
        path.read_text(encoding="utf-8")
    )

    node = data["nodes"][0]
    service = data["services"][0]

    assert node["id"] == "zwave-01"
    assert node["endpoint"]["address"] == "192.168.1.11"

    assert service["id"] == "dns-primary"
    assert service["name"] == "DNS Primary"
    assert service["type"] == "dns"
    assert service["node"] == "zwave-01"
    assert service["port"] == 53