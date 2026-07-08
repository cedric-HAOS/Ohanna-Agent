from pathlib import Path

from plugin.plugin import Plugin
from plugin.plugin_descriptor import PluginDescriptor
from plugin.plugin_loader import PluginLoader
from plugin.plugin_manifest import PluginManifest


class FakePlugin(Plugin):
    @property
    def manifest(self) -> PluginManifest:
        return PluginManifest(name="fake", version="1.0.0")

    def register(self, context: object) -> None:
        pass


class FakeFactory:
    def __init__(self) -> None:
        self.created_descriptors = []

    def create(self, descriptor: PluginDescriptor) -> Plugin:
        self.created_descriptors.append(descriptor)
        return FakePlugin()


def test_plugin_loader_uses_factory() -> None:
    factory = FakeFactory()
    loader = PluginLoader(factory=factory)
    descriptor = PluginDescriptor(name="fake", path=Path("plugins/fake"))

    plugin = loader.load(descriptor)

    assert isinstance(plugin, FakePlugin)
    assert factory.created_descriptors == [descriptor]


def test_plugin_loader_loads_all_descriptors() -> None:
    factory = FakeFactory()
    loader = PluginLoader(factory=factory)

    descriptors = (
        PluginDescriptor(name="one", path=Path("plugins/one")),
        PluginDescriptor(name="two", path=Path("plugins/two")),
    )

    plugins = loader.load_all(descriptors)

    assert len(plugins) == 2
    assert factory.created_descriptors == list(descriptors)