from infrastructure import HealthStatus, Observation


def test_observation_can_be_created() -> None:
    observation = Observation(
        target_name="dns",
        health=HealthStatus.HEALTHY,
        source="dns-checker",
    )

    assert observation.target_name == "dns"
    assert observation.health is HealthStatus.HEALTHY
    assert observation.source == "dns-checker"
    assert observation.message == ""
    assert observation.timestamp is not None
    assert observation.metadata == {}