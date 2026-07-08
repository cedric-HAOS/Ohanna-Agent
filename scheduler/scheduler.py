"""Scheduler orchestration service."""

from __future__ import annotations

from dataclasses import dataclass, field

from scheduler.clock import Clock, SystemClock
from scheduler.task import Task
from scheduler.task_executor import (
    DryRunTaskExecutor,
    TaskExecutionResult,
    TaskExecutor,
)
from scheduler.task_registry import TaskRegistry


@dataclass
class Scheduler:
    """Orchestrate scheduled tasks."""

    clock: Clock = field(default_factory=SystemClock)
    registry: TaskRegistry = field(default_factory=TaskRegistry)
    executor: TaskExecutor = field(default_factory=DryRunTaskExecutor)
    running: bool = field(default=False, init=False)

    def start(self) -> None:
        """Start the scheduler."""
        self.running = True

    def stop(self) -> None:
        """Stop the scheduler."""
        self.running = False

    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler."""
        self.registry.add(task)

    def remove_task(self, task_id: str) -> Task:
        """Remove a task from the scheduler."""
        return self.registry.remove(task_id)

    def get_task(self, task_id: str) -> Task:
        """Return a task by id."""
        return self.registry.get(task_id)

    def list_tasks(self) -> list[Task]:
        """Return all registered tasks ordered by priority."""
        return self.registry.list()

    def due_tasks(self) -> list[Task]:
        """Return enabled tasks due at the scheduler current datetime."""
        return self.registry.due_tasks(self.clock.now())

    def tick(self) -> list[TaskExecutionResult]:
        """Execute due tasks for one scheduler tick."""
        if not self.running:
            return []

        now = self.clock.now()
        return [
           self.executor.execute(task, now)
            for task in self.registry.due_tasks(now)
        ]