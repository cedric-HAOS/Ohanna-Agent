from dataclasses import dataclass
from pathlib import Path

from plugin.plugin_manifest import PluginManifest


@dataclass(frozen=True, slots=True)
class PluginDescriptor:
    """Describes a discovered plugin."""

    name: str
    path: Path
    manifest: PluginManifest | None = None