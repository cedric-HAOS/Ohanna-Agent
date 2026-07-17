"""
Ohanna-Agent

Component:
    Configuration enums

Description:
    Defines shared enums used by configuration models.

Author:
    Cédric Harnois, ChatGPT
"""

from __future__ import annotations

from enum import StrEnum


class Environment(StrEnum):
    """Available runtime environments."""

    DEVELOPMENT = "development"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(StrEnum):
    """Available logging levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
