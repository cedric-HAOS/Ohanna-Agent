from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from plugin.plugin_context import PluginContext
from plugin.plugin_manifest import PluginManifest

if TYPE_CHECKING:
    from observer.observer_result import ObserverResult


class Plugin(ABC):
    """Base contract for every Ohanna-Agent plugin."""

    @property
    @abstractmethod
    def manifest(self) -> PluginManifest:
        """Return the plugin manifest."""

    @abstractmethod
    def register(self, context: PluginContext) -> None:
        """Register the plugin."""

    @abstractmethod
    def execute(
        self,
        **kwargs: Any,
    ) -> ObserverResult:
        """Execute the primary capability of the plugin."""
