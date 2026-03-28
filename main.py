from pawpal_system import Pet, Task, Owner, OwnerPreferences, Scheduler

# --- Setup ---
prefs = OwnerPreferences(wake_time=8, sleep_time=21)
owner = Owner("Jordan", time_available=90, preferences=prefs)

mochi = Pet("Mochi", "dog", "Shiba Inu", 3)
luna = Pet("Luna", "cat", "Domestic Shorthair", 5)

owner.pets.append(mochi)
owner.pets.append(luna)

# --- Tasks for Mochi ---
owner.tasks.append(Task("Morning Walk",  "walk",      30, "high",   mochi))
owner.tasks.append(Task("Breakfast",     "feeding",   10, "high",   mochi))
owner.tasks.append(Task("Training",      "enrichment",20, "medium", mochi))

# --- Tasks for Luna ---
owner.tasks.append(Task("Wet Food",      "feeding",   5,  "high",   luna))
owner.tasks.append(Task("Playtime",      "enrichment",15, "medium", luna))
owner.tasks.append(Task("Brush Coat",    "grooming",  10, "low",    luna))

# --- Generate and print the schedule ---
scheduler = Scheduler(owner)
plan = scheduler.generate_plan()

print("=" * 40)
print(f"  PawPal+ — Daily Schedule for {owner.name}")
print("=" * 40)
print(plan.display())
print()
print(scheduler.explain_plan(plan))
