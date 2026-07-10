"""Dispatcher bridge for plugin observation execution."""

from dataclasses import dataclass

from observer.events import ObservationPublished
from observer.plugin_observation_executor import (
    PluginObservationExecutor,
)
from plugin.plugin_command import PluginCommand


@dataclass(slots=True)
class PluginObservationDispatcher:
    """Dispatch plugin commands through the observation execution pipeline."""

    executor: PluginObservationExecutor

    def execute(
        self,
        command: str,
        arguments: dict[str, object] | None = None,
    ) -> ObservationPublished:
        """Parse and execute a plugin command."""
        plugin_command = self.parse(
            command,
            arguments=arguments,
        )

        return self.executor.execute_command(plugin_command)

    @staticmethod
    def parse(
        command: str,
        *,
        arguments: dict[str, object] | None = None,
    ) -> PluginCommand:
        """Convert a dotted command into a structured plugin command."""
        normalized_command = command.strip()

        if not normalized_command:
            raise ValueError("Plugin command must not be empty.")

        plugin_name, separator, operation = normalized_command.partition(".")

        if not separator or not plugin_name or not operation:
            raise ValueError(
                "Plugin command must use the '<plugin>.<operation>' format."
            )

        return PluginCommand(
            plugin_name=plugin_name,
            operation=operation,
            target_name=plugin_name,
            arguments=dict(arguments or {}),
        )