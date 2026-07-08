"""
Ohanna-Agent

Component:
    Configuration loader

Description:
    Loads the application configuration from a YAML file.

Author:
    Cédric Harnois, ChatGPT
"""

from __future__ import annotations

from pathlib import Path

import yaml

from configuration.configuration import Configuration


class ConfigurationLoader:
    """Loads the application configuration."""

    @staticmethod
    def load(path: Path) -> Configuration:
        """
        Load a configuration from a YAML file.

        Args:
            path: Path to the YAML configuration file.

        Returns:
            A validated Configuration instance.
        """
        with path.open("r", encoding="utf-8") as config_file:
            data = yaml.safe_load(config_file) or {}

        return Configuration.model_validate(data)