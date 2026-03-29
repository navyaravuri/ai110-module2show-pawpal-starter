import streamlit as st
from pawpal_system import Owner, Pet, Task, OwnerPreferences, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Session state: initialize the Owner once per session ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan", time_available=90)

owner = st.session_state.owner  # convenience alias

# ── Owner info ────────────────────────────────────────────────────────────────
st.subheader("Owner")
col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Your name", value=owner.name)
with col2:
    time_available = st.number_input("Minutes available today", min_value=10, max_value=480, value=owner.time_available)

if st.button("Update owner"):
    owner.update_info(name=owner_name, time_available=int(time_available))
    st.success(f"Updated: {owner.name}, {owner.time_available} min available.")

st.divider()

# ── Add a Pet ─────────────────────────────────────────────────────────────────
st.subheader("Add a Pet")

with st.form("add_pet_form", clear_on_submit=True):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        pet_name = st.text_input("Name", value="Mochi")
    with col2:
        species = st.selectbox("Species", ["dog", "cat", "other"])
    with col3:
        breed = st.text_input("Breed", value="Shiba Inu")
    with col4:
        age = st.number_input("Age", min_value=0, max_value=30, value=2)
    submitted = st.form_submit_button("Add pet")

if submitted:
    new_pet = Pet(name=pet_name, species=species, breed=breed, age=int(age))
    owner.pets.append(new_pet)
    st.success(f"Added {new_pet.name} the {new_pet.species}!")

if owner.pets:
    st.markdown("**Your pets:**")
    pet_rows = [{"Name": p.name, "Species": p.species, "Breed": p.breed, "Age": p.age} for p in owner.pets]
    st.table(pet_rows)
else:
    st.info("No pets yet. Add one above.")

st.divider()

# ── Add a Task ────────────────────────────────────────────────────────────────
st.subheader("Add a Task")

if not owner.pets:
    st.warning("Add a pet first before creating tasks.")
else:
    pet_names = [p.name for p in owner.pets]

    with st.form("add_task_form", clear_on_submit=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            task_name = st.text_input("Task", value="Morning Walk")
        with col2:
            category = st.selectbox("Category", ["walk", "feeding", "meds", "grooming", "enrichment"])
        with col3:
            duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
        with col4:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

        col5, col6 = st.columns(2)
        with col5:
            selected_pet_name = st.selectbox("For which pet?", pet_names)
        with col6:
            frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

        task_submitted = st.form_submit_button("Add task")

    if task_submitted:
        target_pet = next(p for p in owner.pets if p.name == selected_pet_name)
        new_task = Task(
            name=task_name,
            category=category,
            duration=int(duration),
            priority=priority,
            pet=target_pet,
            frequency=frequency,
        )
        owner.tasks.append(new_task)
        target_pet.add_task(new_task)
        st.success(f"Added '{new_task.name}' for {target_pet.name} ({frequency}).")

    # ── Filter controls ───────────────────────────────────────────────────────
    if owner.tasks:
        st.markdown("**Filter tasks**")
        col1, col2 = st.columns(2)
        with col1:
            filter_pet = st.selectbox("Filter by pet", ["All"] + [p.name for p in owner.pets])
        with col2:
            filter_status = st.selectbox("Filter by status", ["All", "Pending", "Completed"])

        scheduler = Scheduler(owner)
        filtered = owner.tasks

        if filter_pet != "All":
            filtered = scheduler.filter_tasks(filtered, pet_name=filter_pet)
        if filter_status == "Pending":
            filtered = scheduler.filter_tasks(filtered, completed=False)
        elif filter_status == "Completed":
            filtered = scheduler.filter_tasks(filtered, completed=True)

        if filtered:
            task_rows = [
                {
                    "Task": t.name,
                    "Pet": t.pet.name,
                    "Category": t.category,
                    "Duration (min)": t.duration,
                    "Priority": t.priority,
                    "Frequency": t.frequency,
                    "Status": "Done" if t.is_completed else "Pending",
                }
                for t in filtered
            ]
            st.table(task_rows)
        else:
            st.info("No tasks match the current filter.")
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

# ── Generate Schedule ─────────────────────────────────────────────────────────
st.subheader("Generate Schedule")

if st.button("Build today's plan"):
    if not owner.tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        scheduler = Scheduler(owner)
        plan = scheduler.generate_plan()

        # ── Conflict warnings ─────────────────────────────────────────────────
        conflicts = scheduler.detect_conflicts(plan.scheduled_tasks)
        if conflicts:
            for msg in conflicts:
                st.warning(msg)
        else:
            st.success("No scheduling conflicts detected.")

        # ── Sorted schedule table ─────────────────────────────────────────────
        sorted_tasks = scheduler.sort_by_time(plan.scheduled_tasks)
        if sorted_tasks:
            st.markdown(f"**Scheduled — {plan.total_time} min of {owner.time_available} min used**")
            schedule_rows = [
                {
                    "Time": f"{t.start_time.strftime('%I:%M %p')} – {t.end_time.strftime('%I:%M %p')}",
                    "Task": t.name,
                    "Pet": t.pet.name,
                    "Duration (min)": t.duration,
                    "Priority": t.priority,
                    "Status": "Done" if t.is_completed else "Pending",
                }
                for t in sorted_tasks
            ]
            st.table(schedule_rows)

        # ── Skipped tasks ─────────────────────────────────────────────────────
        if plan.skipped_tasks:
            st.markdown("**Skipped — not enough time remaining**")
            for t in plan.skipped_tasks:
                st.warning(f"{t.name} ({t.pet.name}, {t.duration} min, {t.priority} priority)")

        # ── Plan explanation ──────────────────────────────────────────────────
        with st.expander("Why was the plan built this way?"):
            st.markdown(scheduler.explain_plan(plan))
