from datetime import timedelta

from observer import Observation, ObservationRuntime
from observer.checks import FakeCheck


def test_observation_stores_identifier() -> None:
    observation = Observation(
        id="dns-google",
        display_name="DNS Google",
        check=FakeCheck(),
    )

    assert observation.id == "dns-google"


def test_observation_stores_name() -> None:
    observation = Observation(
        id="dns-google",
        display_name="DNS Google",
        check=FakeCheck(),
    )

    assert observation.display_name == "DNS Google"


def test_observation_stores_check() -> None:
    check = FakeCheck()

    observation = Observation(
        id="dns-google",
        display_name="DNS Google",
        check=check,
    )

    assert observation.check is check

def test_observation_default_enabled() -> None:
    observation = Observation(
        id="dns-google",
        display_name="DNS Google",
        check=FakeCheck(),
    )

    assert observation.enabled is True

def test_observation_default_retries() -> None:
    observation = Observation(
        id="dns-google",
        display_name="DNS Google",
        check=FakeCheck(),
    )

    assert observation.retries == 0

def test_observation_default_runtime() -> None:
    observation = Observation(
        id="dns-google",
        display_name="DNS Google",
        check=FakeCheck(),
    )

    assert isinstance(observation.runtime, ObservationRuntime)


def test_observation_default_interval() -> None:
    observation = Observation(
        id="dns-google",
        display_name="DNS Google",
        check=FakeCheck(),
    )

    assert observation.interval == timedelta(minutes=1)


def test_observation_default_timeout() -> None:
    observation = Observation(
        id="dns-google",
        display_name="DNS Google",
        check=FakeCheck(),
    )

    assert observation.timeout == timedelta(seconds=5)