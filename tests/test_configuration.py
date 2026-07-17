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

import pytest
from pydantic import ValidationError

from configuration.enums import Environment, LogLevel
from configuration.loader import ConfigurationLoader


def test_load_shikamaru_configuration() -> None:
    """Load the default Shikamaru YAML configuration."""
    configuration = ConfigurationLoader.load(Path("config/shikamaru.yaml"))

    assert configuration.version == 1
    assert configuration.agent.name == "Shikamaru"
    assert configuration.agent.environment == Environment.PRODUCTION
    assert configuration.mqtt.host == "ha-green.ohanna.lan"
    assert configuration.mqtt.port == 1883
    assert configuration.logging.level == LogLevel.INFO
    assert configuration.health.enabled is True
    assert configuration.health.interval_seconds == 30
    assert configuration.plugins.enabled is True
    assert str(configuration.plugins.directory) == "plugins"
    assert configuration.vision.enabled is True
    assert str(configuration.vision.observation_url) == (
        "http://127.0.0.1:8000/api/observations"
    )
    assert configuration.vision.timeout_seconds == 5.0


def test_configuration_accepts_schema_version_one(
    tmp_path: Path,
) -> None:
    """Accept the supported configuration schema version."""
    config_path = tmp_path / "shikamaru.yaml"
    config_path.write_text(
        "version: 1\n",
        encoding="utf-8",
    )

    configuration = ConfigurationLoader.load(config_path)

    assert configuration.version == 1


def test_configuration_rejects_unknown_schema_version(
    tmp_path: Path,
) -> None:
    """Reject a configuration schema version not supported by the agent."""
    config_path = tmp_path / "shikamaru.yaml"
    config_path.write_text(
        "version: 2\n",
        encoding="utf-8",
    )

    with pytest.raises(ValidationError, match="version"):
        ConfigurationLoader.load(config_path)


def test_configuration_uses_schema_version_one_by_default(
    tmp_path: Path,
) -> None:
    """Use schema version one when the version field is omitted."""
    config_path = tmp_path / "shikamaru.yaml"
    config_path.write_text(
        "{}\n",
        encoding="utf-8",
    )

    configuration = ConfigurationLoader.load(config_path)

    assert configuration.version == 1
