"""Ohanna-Vision export configuration."""

from pydantic import Field, HttpUrl, PositiveFloat

from configuration.base import Config


class VisionConfig(Config):
    """Configuration used to export observations to Ohanna-Vision."""

    enabled: bool = True
    observation_url: HttpUrl = Field(
        default=HttpUrl("http://127.0.0.1:8000/api/observations")
    )
    timeout_seconds: PositiveFloat = 5.0
