"""In-memory synchronous event bus."""

from collections import defaultdict
from collections.abc import Callable

from core.event_subscription import EventSubscription
from core.events import event


class EventBus:
    """Simple synchronous in-memory event bus."""

    def __init__(self) -> None:
        self._subscriptions: dict[type[event.Event], list[EventSubscription]] = (
            defaultdict(list)
        )

    def subscribe(
        self,
        event_type: type[event.Event],
        callback: Callable[[event.Event], None],
    ) -> None:
        """Subscribe a callback to an event type."""
        subscription = EventSubscription(
            event_type=event_type,
            callback=callback,
        )

        if subscription not in self._subscriptions[event_type]:
            self._subscriptions[event_type].append(subscription)

    def unsubscribe(
        self,
        event_type: type[event.Event],
        callback: Callable[[event.Event], None],
    ) -> None:
        """Remove a callback from an event type."""
        self._subscriptions[event_type] = [
            subscription
            for subscription in self._subscriptions[event_type]
            if subscription.callback is not callback
        ]

    def publish(self, event_instance: event.Event) -> None:
        """Publish an event to all subscribers."""
        event_type = type(event_instance)

        for subscription in list(self._subscriptions[event_type]):
            subscription.callback(event_instance)