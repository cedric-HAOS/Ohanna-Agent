"""Tests for the Shikamaru application runtime."""

from application import Application
from core.dispatcher import CommandDispatcher
from core.events import EventBus
from core.plugins import PluginManager
from core.scheduler import Scheduler
from core.services import ServiceRegistry


def test_application_creates_service_registry() -> None:
    """Application creates a service registry."""
    app = Application()

    assert isinstance(app.services, ServiceRegistry)


def test_application_creates_core_services() -> None:
    """Application creates core services."""
    app = Application()

    assert isinstance(app.event_bus, EventBus)
    assert isinstance(app.scheduler, Scheduler)
    assert isinstance(app.plugin_manager, PluginManager)
    assert isinstance(app.command_dispatcher, CommandDispatcher)


def test_application_registers_service_registry() -> None:
    """Application registers the service registry."""
    app = Application()

    assert app.services.get(ServiceRegistry) is app.services


def test_application_registers_event_bus() -> None:
    """Application registers the event bus."""
    app = Application()

    assert app.services.get(EventBus) is app.event_bus


def test_application_registers_scheduler() -> None:
    """Application registers the scheduler."""
    app = Application()

    assert app.services.get(Scheduler) is app.scheduler


def test_application_registers_plugin_manager() -> None:
    """Application registers the plugin manager."""
    app = Application()

    assert app.services.get(PluginManager) is app.plugin_manager


def test_application_registers_command_dispatcher() -> None:
    """Application registers the command dispatcher."""
    app = Application()

    assert app.services.get(CommandDispatcher) is app.command_dispatcher