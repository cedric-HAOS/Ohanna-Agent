from typing import Protocol

from plugin.plugin_descriptor import PluginDescriptor


class DiscoveryProvider(Protocol):
    """Contract for plugin discovery providers."""

    def discover(self) -> tuple[PluginDescriptor, ...]:
        """Discover available plugins."""
