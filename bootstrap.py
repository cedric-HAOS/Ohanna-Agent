"""Production bootstrap for Ohanna-Agent."""

from __future__ import annotations

from datetime import timedelta
from pathlib import Path

from builder import (
    DNSConfigurationBuilder,
    InfrastructureBuilder,
)
from configuration.infrastructure_validator import (
    InfrastructureValidator,
)
from configuration.loader import ConfigurationLoader
from core.events import EventBus
from infrastructure import InfrastructureRuntime
from infrastructure.infrastructure_health_manager import (
    InfrastructureHealthManager,
)
from loader import DNSConfigLoader, InfrastructureLoader
from observer import (
    InfrastructureObservationMapper,
    ObservationEngine,
    ObservationEventPublisher,
    ObservationExportHandler,
    ObservationExportPipeline,
    ObservationPublished,
    ObserverResultMapper,
    PluginObservationDispatcher,
    PluginObservationExecutor,
)
from observer.exporters import (
    HttpVisionClient,
    VisionClient,
    VisionObservationExporter,
    VisionObservationMapper,
)
from plugin.plugin_context import PluginContext
from plugin.plugin_manager import PluginManager
from plugins.dns.configured_dns_check import ConfiguredDNSCheck
from plugins.dns.dns_plugin import DNSPlugin
from production_agent import ProductionAgent
from scheduler import (
    DispatcherTaskExecutor,
    IntervalTrigger,
    Scheduler,
    Task,
)
from scheduler.clock import Clock, SystemClock


def build_production_agent(
    *,
    application_config_path: Path = Path("config/shikamaru.yaml"),
    infrastructure_config_path: Path = Path("config/infrastructure.yaml"),
    dns_config_path: Path = Path("config/plugins/dns.yaml"),
    vision_client: VisionClient | None = None,
    clock: Clock | None = None,
) -> ProductionAgent:
    """Build the complete production Ohanna-Agent runtime."""
    configuration = ConfigurationLoader.load(application_config_path)

    infrastructure_config = InfrastructureLoader().load(infrastructure_config_path)
    InfrastructureValidator().validate(infrastructure_config)
    infrastructure = InfrastructureBuilder().build(infrastructure_config)
    infrastructure_runtime = InfrastructureRuntime.from_infrastructure(infrastructure)

    dns_plugin_config = DNSConfigLoader().load(dns_config_path)
    dns_config = DNSConfigurationBuilder().build(
        infrastructure,
        dns_plugin_config,
    )

    enabled_servers = [server for server in dns_config.servers if server.enabled]

    if len(enabled_servers) != 1:
        raise ValueError(
            "The first production deployment requires exactly one enabled DNS server."
        )

    if not dns_config.queries:
        raise ValueError(
            "The production DNS configuration must declare at least one query."
        )

    event_bus = EventBus()

    resolved_vision_client = vision_client

    if resolved_vision_client is None:
        if not configuration.vision.enabled:
            raise ValueError(
                "Ohanna-Vision export must be enabled for the production bootstrap."
            )

        resolved_vision_client = HttpVisionClient(
            observation_url=str(
                configuration.vision.observation_url
            ),
            infrastructure_url=str(
                configuration.vision.infrastructure_url
            ),
            timeout_seconds=(
                configuration.vision.timeout_seconds
            ),
        )

    export_handler = ObservationExportHandler(
        pipeline=ObservationExportPipeline(
            exporters=[
                VisionObservationExporter(
                    client=resolved_vision_client,
                    mapper=VisionObservationMapper(),
                )
            ]
        )
    )

    event_bus.subscribe(
        ObservationPublished,
        export_handler.handle,
    )

    observation_engine = ObservationEngine(
        health_manager=InfrastructureHealthManager(
            runtime=infrastructure_runtime,
        ),
        mapper=InfrastructureObservationMapper(),
        result_mapper=ObserverResultMapper(),
        publisher=ObservationEventPublisher(
            event_publisher=event_bus,
        ),
    )

    plugin_context = PluginContext(
        event_bus=event_bus,
        scheduler=None,
        dispatcher=None,
        memory=None,
        capability_manager=None,
        configuration=configuration,
        runtime=infrastructure_runtime,
    )

    plugin_manager = PluginManager(
        context=plugin_context,
    )

    dns_server = enabled_servers[0]

    plugin_manager.register(
        DNSPlugin(
            check=ConfiguredDNSCheck(
                server=dns_server.address,
            ),
            config=dns_config,
        )
    )

    plugin_executor = PluginObservationExecutor(
        plugin_manager=plugin_manager,
        observation_engine=observation_engine,
    )
    dispatcher = PluginObservationDispatcher(
        executor=plugin_executor,
    )

    resolved_clock = clock or SystemClock()

    scheduler = Scheduler(
        clock=resolved_clock,
        executor=DispatcherTaskExecutor(
            dispatcher=dispatcher,
        ),
        event_bus=event_bus,
    )

    start_at = resolved_clock.now()

    for hostname in dns_config.queries:
        scheduler.add_task(
            Task(
                name=(f"Resolve {hostname} through {dns_server.name}"),
                command="dns.resolve",
                trigger=IntervalTrigger(
                    interval=timedelta(seconds=(dns_plugin_config.interval_seconds)),
                    start_at=start_at,
                ),
                arguments={
                    "hostname": hostname,
                },
                metadata={
                    "service_id": dns_server.name,
                    "server": dns_server.address,
                },
            )
        )

    return ProductionAgent(
        scheduler=scheduler,
    )
