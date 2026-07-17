from dataclasses import dataclass
from datetime import datetime

from observer.observation_state import ObservationState
from observer.observer_result import ObserverResult


@dataclass(slots=True)
class ObservationRuntime:
    """Runtime information for an observation."""

    state: ObservationState = ObservationState.IDLE

    last_result: ObserverResult | None = None

    last_execution: datetime | None = None

    next_execution: datetime | None = None
