import pytest
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
