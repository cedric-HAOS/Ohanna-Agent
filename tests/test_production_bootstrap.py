from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from bootstrap import build_production_agent
from scheduler.clock import FakeClock


@dataclass
class FakeVisionClient:
    """Capture data exported by the production bootstrap."""

    operations: list[tuple[str, dict[str, Any]]] = field(default_factory=list)

    def send_observation(
        self,
        payload: dict[str, Any],
    ) -> None:
        self.operations.append(("observation", payload))

    def send_infrastructure(
        self,
        payload: dict[str, Any],
    ) -> None:
        self.operations.append(("infrastructure", payload))


def test_production_bootstrap_builds_dns_task() -> None:
    clock = FakeClock(
        current_time=datetime(
            2026,
            7,
            15,
            12,
            0,
            tzinfo=UTC,
        )
    )

    agent = build_production_agent(
        application_config_path=Path("config/shikamaru.yaml"),
        infrastructure_config_path=Path("config/infrastructure.yaml"),
        dns_config_path=Path("config/plugins/dns.yaml"),
        vision_client=FakeVisionClient(),
        clock=clock,
    )

    tasks = agent.scheduler.list_tasks()

    assert len(tasks) == 1
    assert tasks[0].command == "dns.resolve"
    assert tasks[0].arguments == {
        "hostname": "example.com",
    }
    assert tasks[0].metadata == {
        "service_id": "dns-primary",
        "server": "192.168.1.10",
    }
    assert agent.infrastructure_retry_seconds == 10.0
    assert agent.infrastructure_refresh_seconds == 300.0
    assert agent.infrastructure_payload is not None
    assert len(agent.infrastructure_payload["topology"]["devices"]) == 9
    assert len(agent.infrastructure_payload["topology"]["links"]) == 8


def test_production_bootstrap_exports_infrastructure_before_observation() -> None:
    clock = FakeClock(
        current_time=datetime(
            2026,
            7,
            15,
            12,
            0,
            tzinfo=UTC,
        )
    )
    vision_client = FakeVisionClient()

    agent = build_production_agent(
        vision_client=vision_client,
        clock=clock,
    )

    agent.start()
    agent.tick()
    agent.stop()

    assert [operation for operation, _payload in vision_client.operations] == [
        "infrastructure",
        "observation",
    ]

    infrastructure_payload = vision_client.operations[0][1]

    assert infrastructure_payload["infrastructure_id"] == ("ohana-house")
    assert len(infrastructure_payload["topology"]["devices"]) == 9
    assert len(infrastructure_payload["topology"]["links"]) == 8
    assert len(infrastructure_payload["topology"]["layouts"]) == 1

    observation_payload = vision_client.operations[1][1]

    assert observation_payload["node_id"] == "infra-01"
    assert observation_payload["service_id"] == "dns-primary"
    assert observation_payload["capability_id"] == "dns.resolve"
    assert observation_payload["status"] in {
        "healthy",
        "unavailable",
    }
    assert observation_payload["metadata"]["hostname"] == ("example.com")
    assert observation_payload["metadata"]["server"] == ("192.168.1.10")
