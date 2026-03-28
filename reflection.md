# PawPal+ Project Reflection

## 1. System Design

### Core User Actions

- Enter owner and pet info — input basic profile details about themselves and their pet to personalize the experience.

- Add/edit care tasks — create and modify tasks (walks, feeding, meds, etc.) with at minimum a duration and priority level.

- Generate a daily schedule/plan — trigger the scheduler to produce a prioritized daily plan based on their constraints, and see an explanation of why the plan was chosen that way.

### Building Blocks

| Component            | Type        | Name                  | Description                                                                 |
|---------------------|------------|-----------------------|-----------------------------------------------------------------------------|
| OwnerPreferences     | Attribute  | wake_time             | Hour to start scheduling (24h format, default = 7)                          |
| OwnerPreferences     | Attribute  | sleep_time            | Hour to stop scheduling (24h format, default = 22)                          |
| OwnerPreferences     | Attribute  | avoid_back_to_back    | Whether to avoid scheduling tasks consecutively                             |
| Pet                  | Attribute  | name                  | Pet’s name                                                                  |
| Pet                  | Attribute  | species               | Type of animal (e.g., dog, cat)                                             |
| Pet                  | Attribute  | breed                 | Pet breed                                                                   |
| Pet                  | Attribute  | age                   | Pet age                                                                     |
| Pet                  | Method     | update_info()         | Updates pet attributes dynamically                                          |
| Task                 | Attribute  | name                  | Task name                                                                   |
| Task                 | Attribute  | category              | Task category (walk, feeding, etc.)                                         |
| Task                 | Attribute  | duration              | Duration in minutes                                                         |
| Task                 | Attribute  | priority              | Priority label ("low", "medium", "high")                                   |
| Task                 | Attribute  | pet                   | The pet this task belongs to                                                |
| Task                 | Attribute  | is_completed          | Whether the task is completed                                               |
| Task                 | Attribute  | start_time            | Start time assigned by scheduler                                            |
| Task                 | Attribute  | end_time              | End time assigned by scheduler                                              |
| Task                 | Property   | priority_level        | Numeric priority derived from PRIORITY_MAP                                  |
| Task                 | Method     | edit()                | Updates task attributes                                                     |
| Task                 | Method     | mark_complete()       | Marks task as completed                                                     |
| Owner                | Attribute  | name                  | Owner’s name                                                                |
| Owner                | Attribute  | time_available        | Total available time in minutes                                             |
| Owner                | Attribute  | preferences           | OwnerPreferences object                                                     |
| Owner                | Attribute  | pets                  | List of pets owned                                                          |
| Owner                | Attribute  | tasks                 | List of tasks                                                               |
| Owner                | Method     | update_info()         | Updates owner attributes                                                    |
| DailyPlan            | Attribute  | scheduled_tasks       | List of tasks included in the plan                                          |
| DailyPlan            | Attribute  | skipped_tasks         | List of tasks not included                                                  |
| DailyPlan            | Attribute  | total_time            | Total time of scheduled tasks                                               |
| DailyPlan            | Method     | display()             | Returns formatted plan for UI                                               |
| DailyPlan            | Method     | get_summary()         | Returns summary explanation of the plan                                     |
| Scheduler            | Attribute  | owner                 | Owner object used for scheduling                                            |
| Scheduler            | Method     | generate_plan()       | Creates a plan, assigns start/end times, returns DailyPlan                  |
| Scheduler            | Method     | explain_plan(plan)    | Explains why tasks were scheduled or skipped                                |

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design included five main classes: Pet, Task, Owner, DailyPlan, and Scheduler.

- Pet was responsible for storing basic pet information (name, species, breed, age) and allowing updates to that data.
- Task represented individual pet care activities, with attributes like duration, priority, and completion status, along with methods to edit or mark tasks as complete.
- Owner acted as the central entity, holding the pet and a list of tasks, as well as constraints like available time and preferences.
- DailyPlan was designed to store the results of scheduling, including which tasks were scheduled or skipped and the total time used, and to provide a formatted display and summary.
- Scheduler handled the core logic, taking the owner’s tasks and constraints to generate a daily plan and explain the reasoning behind it.

Overall, the design separated data (Pet, Task, Owner) from planning logic (Scheduler) and output representation (DailyPlan).

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, the design did change during implementation.

One key change was updating the **Owner** class from holding a single pet to supporting **multiple pets** using a list. This was done to make the system more realistic and flexible, since many owners have more than one pet. It also allowed tasks to be better organized and associated with specific pets.

Another change was adding **start_time and end_time attributes to Task**, so the scheduler could assign actual time slots instead of just ordering tasks. This made the daily plan more practical and easier to understand for users.

These changes improved the system’s flexibility and made the scheduling output more meaningful.


---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers three main constraints: the owner's total available time, task priority (low/medium/high), and the owner's wake and sleep hours. Priority was the most important because a pet's medication or feeding should always come before optional tasks like grooming. Time availability came second, since the schedule has to fit within the owner's day. Wake and sleep hours set the boundaries so nothing gets scheduled at unrealistic times.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler uses a greedy approach — it picks tasks in priority order and adds each one if it fits, skipping it if not. This means a long low-priority task won't block a short high-priority one, but it also means the schedule isn't perfectly optimized. For example, two medium tasks might fit where one large high-priority task was skipped. This tradeoff is reasonable because pet care schedules don't need to be mathematically perfect — they just need to make sure the most important tasks get done first within the time available.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
