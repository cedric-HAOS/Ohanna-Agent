"""Tests for the Shikamaru application runtime."""

from application import Application
from core.dispatcher import CommandDispatcher
from core.events import EventBus
from core.plugins import PluginManager
from core.services import ServiceRegistry
from scheduler import DispatcherTaskExecutor, Scheduler


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


def test_application_scheduler_is_initially_stopped() -> None:
    """Application scheduler is stopped by default."""
    app = Application()

    assert app.scheduler.runtime.running is False


def test_application_scheduler_uses_dispatcher_task_executor() -> None:
    """Application scheduler uses a dispatcher task executor."""
    app = Application()

    assert isinstance(app.scheduler.executor, DispatcherTaskExecutor)


def test_application_start_starts_scheduler() -> None:
    """Application start starts the scheduler."""
    app = Application()

    app.start()

    assert app.scheduler.runtime.running is True


def test_application_stop_stops_scheduler() -> None:
    """Application stop stops the scheduler."""
    app = Application()

    app.start()
    app.stop()

    assert app.scheduler.runtime.running is False


def test_application_tick_calls_scheduler() -> None:
    """Application tick delegates to the scheduler."""
    app = Application()

    app.start()

    assert app.tick() == []