import pytest
from datetime import time, date, timedelta
from pawpal_system import Pet, Task, Owner, OwnerPreferences, Scheduler, DailyPlan


# --- Fixtures ---

@pytest.fixture
def pet():
    return Pet("Mochi", "dog", "Shiba Inu", 3)

@pytest.fixture
def owner(pet):
    o = Owner("Jordan", time_available=60)
    o.pets.append(pet)
    return o

@pytest.fixture
def tasks(pet):
    return [
        Task("Morning Walk", "walk",      30, "high",   pet),
        Task("Breakfast",    "feeding",   10, "high",   pet),
        Task("Grooming",     "grooming",  15, "medium", pet),
    ]


# --- Task tests ---

def test_task_priority_level(pet):
    t = Task("Walk", "walk", 20, "high", pet)
    assert t.priority_level == 3

def test_task_mark_complete(pet):
    t = Task("Walk", "walk", 20, "high", pet)
    t.mark_complete()
    assert t.is_completed is True

def test_task_edit(pet):
    t = Task("Walk", "walk", 20, "high", pet)
    t.edit(duration=45, priority="low")
    assert t.duration == 45
    assert t.priority == "low"


# --- Pet tests ---

def test_pet_update_info(pet):
    pet.update_info(name="Kuma", age=4)
    assert pet.name == "Kuma"
    assert pet.age == 4


# --- Owner tests ---

def test_owner_update_info(owner):
    owner.update_info(name="Alex", time_available=120)
    assert owner.name == "Alex"
    assert owner.time_available == 120

def test_owner_tasks_list(owner, tasks):
    for t in tasks:
        owner.tasks.append(t)
    assert len(owner.tasks) == 3


# --- Scheduler tests ---

def test_scheduler_schedules_high_priority_first(owner, tasks):
    for t in tasks:
        owner.tasks.append(t)
    plan = Scheduler(owner).generate_plan()
    assert plan.scheduled_tasks[0].priority == "high"

def test_scheduler_respects_time_budget(pet):
    owner = Owner("Jordan", time_available=20)
    owner.pets.append(pet)
    owner.tasks.append(Task("Long Walk", "walk", 60, "high", pet))
    plan = Scheduler(owner).generate_plan()
    assert len(plan.scheduled_tasks) == 0
    assert len(plan.skipped_tasks) == 1

def test_scheduler_skips_completed_tasks(owner, tasks):
    for t in tasks:
        owner.tasks.append(t)
    tasks[0].mark_complete()
    plan = Scheduler(owner).generate_plan()
    scheduled_names = [t.name for t in plan.scheduled_tasks]
    assert tasks[0].name not in scheduled_names

def test_scheduler_assigns_start_and_end_times(owner, tasks):
    for t in tasks:
        owner.tasks.append(t)
    plan = Scheduler(owner).generate_plan()
    for task in plan.scheduled_tasks:
        assert task.start_time is not None
        assert task.end_time is not None

def test_scheduler_total_time(owner, tasks):
    for t in tasks:
        owner.tasks.append(t)
    plan = Scheduler(owner).generate_plan()
    expected = sum(t.duration for t in plan.scheduled_tasks)
    assert plan.total_time == expected


# --- DailyPlan tests ---

def test_daily_plan_display_empty():
    plan = DailyPlan()
    assert "No tasks" in plan.display()

def test_daily_plan_get_summary(owner, tasks):
    for t in tasks:
        owner.tasks.append(t)
    plan = Scheduler(owner).generate_plan()
    summary = plan.get_summary()
    assert "Scheduled" in summary


# --- Two new tests ---

def test_mark_complete_changes_status(pet):
    """Task Completion: mark_complete() should flip is_completed to True."""
    task = Task("Evening Walk", "walk", 20, "medium", pet)
    assert task.is_completed is False
    task.mark_complete()
    assert task.is_completed is True

def test_add_task_increases_pet_task_count(pet):
    """Task Addition: adding a task to a pet should increase its task count."""
    assert len(pet.tasks) == 0
    task = Task("Breakfast", "feeding", 10, "high", pet)
    pet.add_task(task)
    assert len(pet.tasks) == 1


# --- Sorting tests ---

def test_sort_by_time_returns_chronological_order(owner, pet):
    """Sorting: tasks should come back in start_time order, earliest first."""
    t1 = Task("Walk",      "walk",    20, "high",   pet)
    t2 = Task("Grooming",  "grooming",15, "medium", pet)
    t3 = Task("Breakfast", "feeding", 10, "high",   pet)

    t1.start_time = time(9, 0)
    t2.start_time = time(10, 30)
    t3.start_time = time(8, 0)

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time([t1, t2, t3])

    assert sorted_tasks[0].name == "Breakfast"   # 08:00 — earliest
    assert sorted_tasks[1].name == "Walk"         # 09:00
    assert sorted_tasks[2].name == "Grooming"     # 10:30 — latest

def test_sort_by_time_puts_unscheduled_last(owner, pet):
    """Sorting: tasks with no start_time should always appear after scheduled ones."""
    scheduled = Task("Walk",   "walk",    20, "high", pet)
    unscheduled = Task("Bath", "grooming", 15, "low", pet)

    scheduled.start_time = time(8, 0)
    # unscheduled.start_time stays None

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time([unscheduled, scheduled])

    assert sorted_tasks[0].name == "Walk"   # has a time — goes first
    assert sorted_tasks[1].name == "Bath"   # no time — goes last


# --- Recurrence tests ---

def test_daily_task_creates_next_occurrence(owner, pet):
    """Recurrence: completing a daily task should add a new task due tomorrow."""
    task = Task("Morning Walk", "walk", 30, "high", pet, frequency="daily")
    owner.tasks.append(task)

    scheduler = Scheduler(owner)
    next_task = scheduler.complete_task(task)

    assert task.is_completed is True
    assert next_task is not None
    assert next_task.due_date == date.today() + timedelta(days=1)
    assert next_task.is_completed is False
    assert len(owner.tasks) == 2   # original + new occurrence

def test_weekly_task_creates_next_occurrence(owner, pet):
    """Recurrence: completing a weekly task should add a new task due in 7 days."""
    task = Task("Flea Meds", "meds", 10, "high", pet, frequency="weekly")
    owner.tasks.append(task)

    scheduler = Scheduler(owner)
    next_task = scheduler.complete_task(task)

    assert next_task.due_date == date.today() + timedelta(weeks=1)

def test_once_task_creates_no_new_occurrence(owner, pet):
    """Recurrence: completing a one-time task should not add any new task."""
    task = Task("Vet Visit", "meds", 60, "high", pet, frequency="once")
    owner.tasks.append(task)

    scheduler = Scheduler(owner)
    next_task = scheduler.complete_task(task)

    assert next_task is None
    assert len(owner.tasks) == 1   # no new task added


# --- Conflict detection tests ---

def test_detect_conflicts_flags_overlapping_tasks(owner, pet):
    """Conflict Detection: two tasks with overlapping windows should produce a warning."""
    luna = Pet("Luna", "cat", "Domestic Shorthair", 5)

    t1 = Task("Bath Time",  "grooming", 20, "medium", pet)
    t2 = Task("Flea Check", "meds",     15, "medium", luna)

    t1.start_time = time(9, 0);  t1.end_time = time(9, 20)
    t2.start_time = time(9, 10); t2.end_time = time(9, 25)  # overlaps t1

    warnings = Scheduler(owner).detect_conflicts([t1, t2])

    assert len(warnings) == 1
    assert "Bath Time" in warnings[0]
    assert "Flea Check" in warnings[0]

def test_detect_conflicts_no_warning_for_back_to_back(owner, pet):
    """Conflict Detection: tasks that touch but do not overlap should not conflict."""
    t1 = Task("Walk",      "walk",    20, "high", pet)
    t2 = Task("Breakfast", "feeding", 10, "high", pet)

    t1.start_time = time(8, 0);  t1.end_time = time(8, 20)
    t2.start_time = time(8, 20); t2.end_time = time(8, 30)  # starts exactly when t1 ends

    warnings = Scheduler(owner).detect_conflicts([t1, t2])

    assert len(warnings) == 0
