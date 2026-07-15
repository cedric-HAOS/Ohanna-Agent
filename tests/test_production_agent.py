from production_agent import ProductionAgent
from scheduler import Scheduler


def test_production_agent_can_be_created() -> None:
    scheduler = Scheduler()
    agent = ProductionAgent(
        scheduler=scheduler,
    )

    assert agent.scheduler is scheduler
    assert agent.running is False


def test_production_agent_starts_scheduler() -> None:
    scheduler = Scheduler()
    agent = ProductionAgent(
        scheduler=scheduler,
    )

    agent.start()

    assert scheduler.running is True
    assert agent.running is True

    agent.stop()


def test_production_agent_stops_scheduler() -> None:
    scheduler = Scheduler()
    agent = ProductionAgent(
        scheduler=scheduler,
    )
    agent.start()

    agent.stop()

    assert scheduler.running is False
    assert agent.running is False


def test_production_agent_rejects_invalid_tick_interval() -> None:
    scheduler = Scheduler()

    try:
        ProductionAgent(
            scheduler=scheduler,
            tick_interval_seconds=0,
        )
    except ValueError as error:
        assert str(error) == (
            "tick_interval_seconds must be greater than zero."
        )
    else:
        raise AssertionError("ValueError was not raised.")