"""
Ohanna-Agent

Component:
    Configuration

Description:
    Defines the root configuration model.

Author:
    Cédric Harnois, ChatGPT
"""

from __future__ import annotations

from pydantic import Field, PositiveInt

from configuration.agent import AgentConfig
from configuration.base import Config
from configuration.health import HealthConfig
from configuration.logging import LoggingConfig
from configuration.mqtt import MQTTConfig
from configuration.plugins import PluginsConfig
from configuration.vision import VisionConfig


class Configuration(Config):
    """Root configuration model."""

    version: PositiveInt = 1

    agent: AgentConfig = Field(default_factory=AgentConfig)
    mqtt: MQTTConfig = Field(default_factory=MQTTConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    health: HealthConfig = Field(default_factory=HealthConfig)
    plugins: PluginsConfig = Field(default_factory=PluginsConfig)
    vision: VisionConfig = Field(default_factory=VisionConfig)