from dataclasses import dataclass, field
from typing import Any

from observer import (
    Observation,
    ObservationSerializer,
    ObservationStatus,
)
from observer.exporters import VisionObservationExporter


@dataclass
class FakeVisionClient:
    """Fake Ohanna-Vision client used by tests."""

    payloads: list[dict[str, Any]] = field(default_factory=list)

    def send_observation(
        self,
        payload: dict[str, Any],
    ) -> None:
        self.payloads.append(payload)


def build_observation() -> Observation:
    return Observation(
        node="zwave-01",
        service="dns-primary",
        capability="dns",
        status=ObservationStatus.HEALTHY,
        success=True,
        message="DNS resolution succeeded.",
        source="dns-plugin",
        latency_ms=12.5,
        metadata={
            "hostname": "example.com",
            "server": "192.168.1.54",
        },
    )


def test_vision_exporter_can_be_created() -> None:
    client = FakeVisionClient()
    serializer = ObservationSerializer()

    exporter = VisionObservationExporter(
        client=client,
        serializer=serializer,
    )

    assert exporter.client is client
    assert exporter.serializer is serializer


def test_vision_exporter_sends_serialized_observation() -> None:
    client = FakeVisionClient()
    exporter = VisionObservationExporter(
        client=client,
        serializer=ObservationSerializer(),
    )

    observation = build_observation()

    exporter.export(observation)

    assert len(client.payloads) == 1

    payload = client.payloads[0]

    assert payload["node"] == "zwave-01"
    assert payload["service"] == "dns-primary"
    assert payload["capability"] == "dns"
    assert payload["status"] == "healthy"
    assert payload["success"] is True
    assert payload["latency_ms"] == 12.5


def test_vision_exporter_preserves_metadata() -> None:
    client = FakeVisionClient()
    exporter = VisionObservationExporter(
        client=client,
        serializer=ObservationSerializer(),
    )

    exporter.export(build_observation())

    metadata = client.payloads[0]["metadata"]

    assert metadata == {
        "hostname": "example.com",
        "server": "192.168.1.54",
    }


def test_vision_exporter_sends_each_observation() -> None:
    client = FakeVisionClient()
    exporter = VisionObservationExporter(
        client=client,
        serializer=ObservationSerializer(),
    )

    first = build_observation()
    second = build_observation()

    exporter.export(first)
    exporter.export(second)

    assert len(client.payloads) == 2