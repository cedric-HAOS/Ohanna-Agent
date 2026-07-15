from pathlib import Path

import yaml


def test_dns_yaml_exists() -> None:
    path = Path("config/plugins/dns.yaml")

    assert path.exists()


def test_dns_yaml_references_infrastructure_services() -> None:
    path = Path("config/plugins/dns.yaml")

    data = yaml.safe_load(
        path.read_text(encoding="utf-8")
    )

    assert data["services"] == ["dns-primary"]


def test_dns_yaml_declares_queries_and_policy() -> None:
    path = Path("config/plugins/dns.yaml")

    data = yaml.safe_load(
        path.read_text(encoding="utf-8")
    )

    assert data["queries"] == [
        "example.com",
    ]
    assert data["timeout"] == 2.0
    assert data["retries"] == 1
    assert data["policy"]["minimum_healthy_servers"] == 1