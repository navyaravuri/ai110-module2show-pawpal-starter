from dataclasses import dataclass, field
from datetime import time
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

    def update_info(self, **kwargs) -> None:
        """Update one or more pet attributes."""
        pass


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
        pass

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        pass


class Owner:
    def __init__(self, name: str, time_available: int, preferences: Optional[OwnerPreferences] = None):
        self.name = name
        self.time_available = time_available        # total minutes available today
        self.preferences = preferences or OwnerPreferences()
        self.pets: list[Pet] = []
        self.tasks: list[Task] = []

    def update_info(self, **kwargs) -> None:
        """Update owner attributes."""
        pass


class DailyPlan:
    def __init__(self):
        self.scheduled_tasks: list[Task] = []
        self.skipped_tasks: list[Task] = []
        self.total_time: int = 0                    # sum of scheduled task durations in minutes

    def display(self) -> str:
        """Return a formatted string of the plan for the UI."""
        pass

    def get_summary(self) -> str:
        """Return a short explanation of what was planned and why."""
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def generate_plan(self) -> DailyPlan:
        """Sort and filter tasks by priority and available time; assign start/end times; return a DailyPlan."""
        pass

    def explain_plan(self, plan: DailyPlan) -> str:
        """Return a human-readable explanation of why tasks were included or skipped."""
        pass
