from datetime import UTC, datetime, timedelta

from scheduler import (
    DispatcherTaskExecutor,
    IntervalTrigger,
    Task,
    TaskState,
)


class FakeDispatcher:
    def __init__(self) -> None:
        self.executed: list[tuple[str, dict[str, object]]] = []

    def execute(
        self,
        command: str,
        arguments: dict[str, object] | None = None,
    ) -> None:
        self.executed.append((command, arguments or {}))


class FailingDispatcher:
    def execute(
        self,
        command: str,
        arguments: dict[str, object] | None = None,
    ) -> None:
        msg = "dispatcher failed"
        raise RuntimeError(msg)


def test_dispatcher_task_executor_executes_task_command() -> None:
    now = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
    dispatcher = FakeDispatcher()
    executor = DispatcherTaskExecutor(dispatcher)

    task = Task(
        command="health.check",
        trigger=IntervalTrigger(timedelta(seconds=30)),
        arguments={"verbose": True},
    )

    result = executor.execute(task, now)

    assert dispatcher.executed == [("health.check", {"verbose": True})]
    assert result.task_id == task.id
    assert result.command == "health.check"
    assert result.success is True
    assert result.error is None
    assert task.state == TaskState.WAITING
    assert task.last_started_at == now
    assert task.last_finished_at == now
    assert task.execution_count == 1


def test_dispatcher_task_executor_handles_dispatcher_failure() -> None:
    now = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
    dispatcher = FailingDispatcher()
    executor = DispatcherTaskExecutor(dispatcher)

    task = Task(
        command="health.check",
        trigger=IntervalTrigger(timedelta(seconds=30)),
    )

    result = executor.execute(task, now)

    assert result.task_id == task.id
    assert result.command == "health.check"
    assert result.success is False
    assert result.error == "dispatcher failed"
    assert task.state == TaskState.WAITING
    assert task.last_started_at == now
    assert task.last_failed_at == now
    assert task.last_error == "dispatcher failed"
    assert task.execution_count == 1