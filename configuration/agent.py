"""
Ohanna-Agent

Component:
    Agent configuration

Description:
    Defines the configuration model for the agent identity.

Author:
    Cédric Harnois, ChatGPT
"""

from __future__ import annotations

from configuration.enums import Environment
from configuration.base import Config


class AgentConfig(Config):
    """Configuration model for the agent identity."""

    name: str = "Shikamaru"
    environment: Environment = Environment.DEVELOPMENT