from datetime import time
from pawpal_system import Pet, Task, Owner, OwnerPreferences, Scheduler

# --- Setup ---
prefs = OwnerPreferences(wake_time=8, sleep_time=21)
owner = Owner("Jordan", time_available=120, preferences=prefs)

mochi = Pet("Mochi", "dog", "Shiba Inu", 3)
luna  = Pet("Luna",  "cat", "Domestic Shorthair", 5)

owner.pets.append(mochi)
owner.pets.append(luna)

owner.tasks.append(Task("Morning Walk", "walk",    30, "high",   mochi))
owner.tasks.append(Task("Breakfast",    "feeding", 10, "high",   mochi))
owner.tasks.append(Task("Wet Food",     "feeding",  5, "high",   luna))
owner.tasks.append(Task("Bath Time",    "grooming",20, "medium", mochi))
owner.tasks.append(Task("Flea Check",   "meds",    15, "medium", luna))

# --- Generate plan (assigns sequential times — no conflicts yet) ---
scheduler = Scheduler(owner)
plan = scheduler.generate_plan()

print("=" * 45)
print("  Schedule BEFORE manual override")
print("=" * 45)
print(plan.display())
print()

warnings = scheduler.detect_conflicts(plan.scheduled_tasks)
print("Conflicts:", warnings if warnings else "None")
print()

# --- Force an overlap to simulate a real conflict ---
# Override Bath Time and Flea Check to the same window
bath  = next(t for t in plan.scheduled_tasks if t.name == "Bath Time")
flea  = next(t for t in plan.scheduled_tasks if t.name == "Flea Check")

bath.start_time = time(9, 0)
bath.end_time   = time(9, 20)
flea.start_time = time(9, 10)   # starts while Bath Time is still running
flea.end_time   = time(9, 25)

print("=" * 45)
print("  Schedule AFTER manual overlap injected")
print("=" * 45)
print(plan.display())
print()

warnings = scheduler.detect_conflicts(plan.scheduled_tasks)
if warnings:
    print("--- Conflict Warnings ---")
    for w in warnings:
        print(w)
else:
    print("No conflicts detected.")
