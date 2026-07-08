"""Shikamaru application runtime."""

from core.dispatcher import CommandDispatcher
from core.events import EventBus
from core.plugins import PluginManager
from core.scheduler import Scheduler
from core.services import ServiceRegistry


class Application:
    """Main Shikamaru application."""

    def __init__(self) -> None:
        self.services = ServiceRegistry()

        self.event_bus = EventBus()
        self.scheduler = Scheduler(self.event_bus)
        self.plugin_manager = PluginManager(self.services, self.event_bus)
        self.command_dispatcher = CommandDispatcher(self.event_bus)

        self._register_core_services()

    def _register_core_services(self) -> None:
        """Register core services in the service registry."""
        self.services.register(ServiceRegistry, self.services)
        self.services.register(EventBus, self.event_bus)
        self.services.register(Scheduler, self.scheduler)
        self.services.register(PluginManager, self.plugin_manager)
        self.services.register(CommandDispatcher, self.command_dispatcher)