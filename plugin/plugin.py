from abc import ABC, abstractmethod

from plugin.plugin_context import PluginContext
from plugin.plugin_manifest import PluginManifest


class Plugin(ABC):
    """Base contract for every Ohanna-Agent plugin."""

    @property
    @abstractmethod
    def manifest(self) -> PluginManifest:
        """Return the plugin manifest."""

    @abstractmethod
    def register(self, context: PluginContext) -> None:
        """Register the plugin."""