"""Task executor backed by the dispatcher."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from scheduler.task import Task
from scheduler.task_executor import TaskExecutionResult


class DispatcherLike(Protocol):
    """Minimal dispatcher contract required by the scheduler."""

    def execute(
        self,
        command: str,
        arguments: dict[str, object] | None = None,
    ) -> object:
        """Execute a command."""


@dataclass
class DispatcherTaskExecutor:
    """Execute scheduled tasks through the dispatcher."""

    dispatcher: DispatcherLike

    def execute(self, task: Task, now: datetime) -> TaskExecutionResult:
        """Execute a task using the dispatcher."""
        task.mark_started(now)

        try:
            self.dispatcher.execute(task.command, task.arguments)
        except Exception as exc:
            task.mark_failed(now, exc)

            return TaskExecutionResult(
                task_id=task.id,
                command=task.command,
                success=False,
                started_at=now,
                finished_at=now,
                error=str(exc),
            )

        task.mark_finished(now)

        return TaskExecutionResult(
            task_id=task.id,
            command=task.command,
            success=True,
            started_at=now,
            finished_at=now,
        )
