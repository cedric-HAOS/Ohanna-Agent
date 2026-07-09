from pathlib import Path

import yaml

from configuration.infrastructure import InfrastructureConfig


class InfrastructureLoader:
    """Loads an infrastructure configuration from a YAML file."""

    def load(self, path: str | Path) -> InfrastructureConfig:
        """Load an infrastructure configuration."""

        file_path = Path(path)

        data = yaml.safe_load(file_path.read_text(encoding="utf-8"))

        return InfrastructureConfig.model_validate(data)