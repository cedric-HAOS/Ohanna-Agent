"""Ohanna-Vision observation exporter."""

from dataclasses import dataclass

from observer.exporters.vision_client import VisionClient
from observer.observation import Observation
from observer.observation_exporter import ObservationExporter
from observer.observation_serializer import ObservationSerializer


@dataclass(slots=True)
class VisionObservationExporter(ObservationExporter):
    """Exports standard observations to Ohanna-Vision."""

    client: VisionClient
    serializer: ObservationSerializer

    def export(self, observation: Observation) -> None:
        """Serialize and send an observation to Ohanna-Vision."""
        payload = self.serializer.to_dict(observation)

        self.client.send_observation(payload)