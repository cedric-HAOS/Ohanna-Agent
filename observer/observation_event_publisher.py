"""Observation event publisher."""

from dataclasses import dataclass

from observer.event_publisher import EventPublisher
from observer.events import ObservationPublished
from observer.observation import Observation


@dataclass(slots=True)
class ObservationEventPublisher:
    """Publishes observation domain events."""

    event_publisher: EventPublisher

    def publish(self, observation: Observation) -> ObservationPublished:
        """Publish an event for an observation."""
        event = ObservationPublished(
            observation=observation,
        )

        self.event_publisher.publish(event)

        return event
