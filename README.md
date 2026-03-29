# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Features

- **Priority-based scheduling** — tasks are sorted by priority (high → medium → low) before time slots are assigned, ensuring the most critical care always gets scheduled first
- **Time budget enforcement** — the scheduler tracks the owner's available minutes and skips any task that would exceed the remaining budget, never overloading the day
- **Sorting by time** — scheduled tasks are displayed in chronological order using `sort_by_time()`, regardless of the order they were added
- **Filtering by pet or status** — `filter_tasks()` lets you narrow the task list by pet name, completion status, or both at once
- **Daily recurrence** — marking a daily task complete automatically creates a new instance due the following day using `timedelta(days=1)`
- **Weekly recurrence** — marking a weekly task complete creates a new instance due 7 days later using `timedelta(weeks=1)`
- **Conflict detection** — `detect_conflicts()` checks all scheduled tasks for overlapping time windows and returns a plain-language warning for each conflict found, without crashing the program
- **Plan explanation** — `explain_plan()` produces a human-readable summary of why each task was scheduled or skipped
- **Streamlit UI** — owners can add pets and tasks, filter the task list, generate a daily schedule, and see conflict warnings all in one interactive page

---

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

---

## Testing PawPal+

### Run the tests

```bash
python3 -m pytest tests/test_pawpal.py -v
```

### What the tests cover

| Area | What is verified |
|---|---|
| **Task** | Priority level mapping, editing attributes, marking complete |
| **Pet** | Updating info, adding tasks increases task count |
| **Owner** | Updating name and available time |
| **Scheduler — core** | High priority scheduled first, time budget respected, completed tasks skipped, start/end times assigned, total time accurate |
| **Scheduler — sorting** | Tasks returned in chronological order, unscheduled tasks sort to the end |
| **Scheduler — recurrence** | Daily task creates a new task due tomorrow, weekly due in 7 days, one-time task creates nothing |
| **Scheduler — conflicts** | Overlapping windows produce a warning, back-to-back tasks do not |
| **DailyPlan** | Empty plan message, summary string content |

### Confidence level

⭐⭐⭐⭐ (4/5)

The core scheduling logic, sorting, filtering, recurrence, and conflict detection are all covered with 22 passing tests. One star is held back because edge cases like month/year rollovers for recurring tasks, schedules with zero tasks, and the Streamlit UI layer are not yet tested.

---

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
