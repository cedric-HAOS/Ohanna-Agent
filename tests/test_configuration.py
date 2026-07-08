"""
Ohanna-Agent

Component:
    Configuration tests

Description:
    Tests the configuration loading chain.

Author:
    Cédric Harnois, ChatGPT
"""

from __future__ import annotations

from pathlib import Path

from configuration.enums import Environment, LogLevel
from configuration.loader import ConfigurationLoader


def test_load_shikamaru_configuration() -> None:
    """Load the default Shikamaru YAML configuration."""
    configuration = ConfigurationLoader.load(Path("config/shikamaru.yaml"))

    assert configuration.version == 1
    assert configuration.agent.name == "Shikamaru"
    assert configuration.agent.environment == Environment.DEVELOPMENT
    assert configuration.mqtt.host == "localhost"
    assert configuration.mqtt.port == 1883
    assert configuration.logging.level == LogLevel.INFO
    assert configuration.health.enabled is True
    assert configuration.health.interval_seconds == 30
    assert configuration.plugins.enabled is True
    assert str(configuration.plugins.directory) == "plugins"