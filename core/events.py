"""Event bus for internal Shikamaru communication."""

from collections import defaultdict
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


class EventBusError(Exception):
    """Base exception for event bus errors."""


class EventHandlerNotFoundError(EventBusError):
    """Raised when trying to unsubscribe an unknown handler."""


class EventBus:
    """Synchronous event bus used to publish events to subscribers."""

    def __init__(self) -> None:
        self._subscribers: dict[type[object], list[Callable[[object], None]]] = (
            defaultdict(list)
        )

    def subscribe(self, event_type: type[T], handler: Callable[[T], None]) -> None:
        """Subscribe a handler to an event type."""
        self._subscribers[event_type].append(handler)  # type: ignore[arg-type]

    def unsubscribe(self, event_type: type[T], handler: Callable[[T], None]) -> None:
        """Unsubscribe a handler from an event type."""
        handlers = self._subscribers[event_type]

        if handler not in handlers:
            raise EventHandlerNotFoundError(
                f"Handler not found for event: {event_type.__name__}"
            )

        handlers.remove(handler)

    def publish(self, event: object) -> None:
        """Publish an event to all matching subscribers."""
        event_type = type(event)

        for handler in list(self._subscribers[event_type]):
            handler(event)