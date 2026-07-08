from typing import Protocol

from plugin.plugin import Plugin
from plugin.plugin_descriptor import PluginDescriptor


class PluginFactory(Protocol):
    """Contract for plugin factories."""

    def create(self, descriptor: PluginDescriptor) -> Plugin:
        """Create a plugin from a descriptor."""