from pathlib import Path

from configuration.dns import DNSPluginConfig
from loader import DNSConfigLoader


def test_dns_config_loader_loads_dns_yaml() -> None:
    loader = DNSConfigLoader()

    config = loader.load("config/plugins/dns.yaml")

    assert isinstance(config, DNSPluginConfig)
    assert config.services == ["dns-primary"]
    assert config.queries == [
        "example.com",
    ]
    assert config.timeout == 2.0
    assert config.retries == 1
    assert config.policy.minimum_healthy_servers == 1
    assert config.interval_seconds == 60


def test_dns_config_loader_accepts_path_object() -> None:
    loader = DNSConfigLoader()

    config = loader.load(Path("config/plugins/dns.yaml"))

    assert config.services == ["dns-primary"]
