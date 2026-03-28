from dataclasses import dataclass, field
from datetime import time, timedelta, datetime
from typing import Optional


PRIORITY_MAP: dict[str, int] = {"low": 1, "medium": 2, "high": 3}


@dataclass
class OwnerPreferences:
    wake_time: int = 7          # hour to start scheduling (24h clock)
    sleep_time: int = 22        # hour to stop scheduling (24h clock)
    avoid_back_to_back: bool = False   # prefer a break between tasks


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: list["Task"] = field(default_factory=list)

    def add_task(self, task: "Task") -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def update_info(self, **kwargs) -> None:
        """Update one or more pet attributes."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


@dataclass
class Task:
    name: str
    category: str       # e.g. "walk", "feeding", "meds", "grooming", "enrichment"
    duration: int       # in minutes
    priority: str       # "low", "medium", or "high" — use priority_level for comparisons
    pet: Pet            # which pet this task belongs to
    is_completed: bool = False
    start_time: Optional[time] = None   # set by Scheduler after planning
    end_time: Optional[time] = None     # set by Scheduler after planning

    @property
    def priority_level(self) -> int:
        """Return the numeric priority value for sorting (higher = more urgent)."""
        return PRIORITY_MAP.get(self.priority, 0)

    def edit(self, **kwargs) -> None:
        """Update task attributes (duration, priority, etc.)."""
        allowed = {"name", "category", "duration", "priority"}
        for key, value in kwargs.items():
            if key in allowed:
                setattr(self, key, value)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True


class Owner:
    def __init__(self, name: str, time_available: int, preferences: Optional[OwnerPreferences] = None):
        """Initialize an Owner with a name, daily time budget, and optional scheduling preferences."""
        self.name = name
        self.time_available = time_available        # total minutes available today
        self.preferences = preferences or OwnerPreferences()
        self.pets: list[Pet] = []
        self.tasks: list[Task] = []

    def update_info(self, **kwargs) -> None:
        """Update owner attributes."""
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ("pets", "tasks"):
                setattr(self, key, value)


class DailyPlan:
    def __init__(self):
        """Initialize an empty DailyPlan with no scheduled or skipped tasks."""
        self.scheduled_tasks: list[Task] = []
        self.skipped_tasks: list[Task] = []
        self.total_time: int = 0                    # sum of scheduled task durations in minutes

    def display(self) -> str:
        """Return a formatted string of the plan for the UI."""
        if not self.scheduled_tasks:
            return "No tasks scheduled for today."

        lines = ["## Today's PawPal+ Schedule\n"]
        for task in self.scheduled_tasks:
            start = task.start_time.strftime("%I:%M %p") if task.start_time else "TBD"
            end = task.end_time.strftime("%I:%M %p") if task.end_time else "TBD"
            status = "✓" if task.is_completed else "○"
            lines.append(
                f"{status} [{start} – {end}] **{task.name}** "
                f"({task.pet.name}, {task.duration} min, {task.priority} priority)"
            )

        lines.append(f"\n**Total time:** {self.total_time} min")

        if self.skipped_tasks:
            lines.append("\n### Skipped")
            for task in self.skipped_tasks:
                lines.append(
                    f"- {task.name} ({task.pet.name}, {task.duration} min, {task.priority} priority)"
                )

        return "\n".join(lines)

    def get_summary(self) -> str:
        """Return a short explanation of what was planned and why."""
        summary = f"Scheduled {len(self.scheduled_tasks)} task(s) totalling {self.total_time} min."
        if self.skipped_tasks:
            summary += f" Skipped {len(self.skipped_tasks)} task(s) due to time constraints."
        return summary


class Scheduler:
    def __init__(self, owner: Owner):
        """Bind the Scheduler to a specific Owner whose tasks and preferences it will use."""
        self.owner = owner

    def generate_plan(self) -> DailyPlan:
        """Sort and filter tasks by priority and available time; assign start/end times; return a DailyPlan."""
        plan = DailyPlan()
        prefs = self.owner.preferences

        # Option A: pull all tasks directly from owner.tasks
        pending = [t for t in self.owner.tasks if not t.is_completed]
        pending.sort(key=lambda t: (-t.priority_level, t.name))

        cursor = datetime.combine(datetime.today(), time(prefs.wake_time, 0))
        day_end = datetime.combine(datetime.today(), time(prefs.sleep_time, 0))
        budget = self.owner.time_available  # minutes remaining

        for task in pending:
            task_end = cursor + timedelta(minutes=task.duration)
            if task_end <= day_end and task.duration <= budget:
                task.start_time = cursor.time()
                task.end_time = task_end.time()
                plan.scheduled_tasks.append(task)
                plan.total_time += task.duration
                budget -= task.duration
                cursor = task_end
            else:
                task.start_time = None
                task.end_time = None
                plan.skipped_tasks.append(task)

        return plan

    def explain_plan(self, plan: DailyPlan) -> str:
        """Return a human-readable explanation of why tasks were included or skipped."""
        lines = ["### Plan Explanation\n"]

        if plan.scheduled_tasks:
            lines.append("**Scheduled:**")
            for task in plan.scheduled_tasks:
                start = task.start_time.strftime("%I:%M %p") if task.start_time else "TBD"
                lines.append(
                    f"- **{task.name}** ({task.pet.name}): {task.duration} min at {start}, "
                    f"{task.priority} priority."
                )

        if plan.skipped_tasks:
            lines.append("\n**Skipped:**")
            for task in plan.skipped_tasks:
                lines.append(
                    f"- **{task.name}** ({task.pet.name}): {task.duration} min needed — "
                    f"not enough time remaining ({task.priority} priority)."
                )

        lines.append(
            f"\n**Total:** {plan.total_time} min scheduled out of "
            f"{self.owner.time_available} min available."
        )
        return "\n".join(lines)
