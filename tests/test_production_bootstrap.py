from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from bootstrap import build_production_agent
from scheduler.clock import FakeClock


@dataclass
class FakeVisionClient:
    """Capture observations exported by the production bootstrap."""

    payloads: list[dict[str, Any]] = field(
        default_factory=list
    )

    def send_observation(
        self,
        payload: dict[str, Any],
    ) -> None:
        self.payloads.append(payload)


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
        application_config_path=Path(
            "config/shikamaru.yaml"
        ),
        infrastructure_config_path=Path(
            "config/infrastructure.yaml"
        ),
        dns_config_path=Path(
            "config/plugins/dns.yaml"
        ),
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


def test_production_bootstrap_exports_real_dns_observation() -> None:
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

    assert len(vision_client.payloads) == 1

    payload = vision_client.payloads[0]

    assert payload["node_id"] == "infra-01"
    assert payload["service_id"] == "dns-primary"
    assert payload["capability_id"] == "dns.resolve"
    assert payload["status"] in {
        "healthy",
        "unavailable",
    }
    assert payload["metadata"]["hostname"] == "example.com"
    assert payload["metadata"]["server"] == "192.168.1.10"