"""
Ohanna-Agent

Component:
    Logging configuration

Description:
    Defines the configuration model for application logging.

Author:
    Cédric Harnois, ChatGPT
"""

from __future__ import annotations

from configuration.enums import LogLevel
from configuration.base import Config


class LoggingConfig(Config):
    """Configuration model for application logging."""

    level: LogLevel = LogLevel.INFO