"""Shikamaru application runtime."""

from core.application_events import (
    ApplicationStarted,
    ApplicationStopped,
    ApplicationTicked,
)
from core.dispatcher import CommandDispatcher
from core.events import EventBus
from core.plugins import PluginManager
from core.services import ServiceRegistry
from memory import MemoryManager
from scheduler import DispatcherTaskExecutor, Scheduler


class Application:
    """Main Shikamaru application."""

    def __init__(
        self,
        memory: MemoryManager | None = None,
        event_bus: EventBus | None = None,
    ) -> None:
        self.services = ServiceRegistry()

        self.event_bus = event_bus or EventBus()
        self.command_dispatcher = CommandDispatcher(self.event_bus)
        self.memory = memory if memory is not None else MemoryManager()
        self.scheduler = Scheduler(
            executor=DispatcherTaskExecutor(self.command_dispatcher),
            event_bus=self.event_bus,
        )
        self.plugin_manager = PluginManager(self.services, self.event_bus)
        event_bus=self.event_bus
        self._register_core_services()

    def _register_core_services(self) -> None:
        """Register core services in the service registry."""
        self.services.register(ServiceRegistry, self.services)
        self.services.register(EventBus, self.event_bus)
        self.services.register(Scheduler, self.scheduler)
        self.services.register(PluginManager, self.plugin_manager)
        self.services.register(CommandDispatcher, self.command_dispatcher)
        self.services.register(MemoryManager, self.memory)

    def start(self) -> None:
        """Start application services."""
        self.scheduler.start()
        self.event_bus.publish(ApplicationStarted())


    def stop(self) -> None:
        """Stop application services."""
        self.scheduler.stop()
        self.event_bus.publish(ApplicationStopped())


    def tick(self) -> object:
        """Execute one application scheduler tick."""
        result = self.scheduler.tick()
        self.event_bus.publish(ApplicationTicked(result=result))
        return result