"""Ohana-Vision observation exporter."""

from dataclasses import dataclass

from observer.exporters.vision_client import VisionClient
from observer.exporters.vision_observation_mapper import (
    VisionObservationMapper,
)
from observer.observation import Observation
from observer.observation_exporter import ObservationExporter


@dataclass(slots=True)
class VisionObservationExporter(ObservationExporter):
    """Export standard observations to Ohana-Vision."""

    client: VisionClient
    mapper: VisionObservationMapper

    def export(self, observation: Observation) -> None:
        """Map and send an observation to Ohana-Vision."""
        payload = self.mapper.to_payload(observation)

        self.client.send_observation(payload)
