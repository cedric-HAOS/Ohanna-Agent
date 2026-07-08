# tests/test_dns_plugin.py

from plugin.plugin_runtime import PluginState
from plugins.dns.dns_plugin import DNSPlugin


def test_dns_plugin_has_name() -> None:
    plugin = DNSPlugin()

    assert plugin.name == "dns"


def test_dns_plugin_initial_state_is_loaded() -> None:
    plugin = DNSPlugin()

    assert plugin.state == PluginState.LOADED

def test_dns_plugin_manifest() -> None:
    plugin = DNSPlugin()

    manifest = plugin.manifest()

    assert manifest.name == "dns"
    assert manifest.version == "0.1.0"
    assert manifest.description == "DNS capability plugin for Ohanna-Agent."

def test_dns_plugin_register_sets_loaded_state() -> None:
    plugin = DNSPlugin()

    plugin.register()

    assert plugin.state == PluginState.LOADED