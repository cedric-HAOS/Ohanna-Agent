import pytest
from pydantic import ValidationError

from configuration.vision import VisionConfig


def test_vision_config_has_production_defaults() -> None:
    config = VisionConfig()

    assert config.enabled is True
    assert str(config.observation_url) == ("http://127.0.0.1:8000/api/observations")
    assert config.timeout_seconds == 5.0


def test_vision_config_accepts_custom_endpoint() -> None:
    config = VisionConfig(
        enabled=True,
        observation_url=("http://192.168.1.10:8000/api/observations"),
        timeout_seconds=3.0,
    )

    assert str(config.observation_url) == ("http://192.168.1.10:8000/api/observations")
    assert config.timeout_seconds == 3.0


def test_vision_config_rejects_invalid_url() -> None:
    with pytest.raises(ValidationError):
        VisionConfig(
            observation_url="not-a-url",
        )


def test_vision_config_rejects_zero_timeout() -> None:
    with pytest.raises(ValidationError):
        VisionConfig(
            timeout_seconds=0,
        )
