import sys
from pathlib import Path

import pandas as pd
import numpy as np

# Identify the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Allow imports from the project
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import (
    START_DATE,
    END_DATE,
    NUM_DEVELOPERS,
    TOTAL_ACTIVITY_RECORDS,
    RECORDS_PER_DEVELOPER,
    RANDOM_SEED,
)

# Use a reproducible random generator
rng = np.random.default_rng(RANDOM_SEED)

# Define data paths
DATA_DIR = PROJECT_ROOT / "data" / "raw"

DEVELOPER_FILE = DATA_DIR / "cognistream_developers.csv"

# Save test output separately from the original dataset
TEST_ACTIVITY_FILE = DATA_DIR / "cognistream_activity_test.csv"

print("CogniStream workday generator initialized")
print("Developer file exists:", DEVELOPER_FILE.exists())
print("Target records:", TOTAL_ACTIVITY_RECORDS)
print("Records per developer:", RECORDS_PER_DEVELOPER)
print("Simulation period:", START_DATE, "to", END_DATE)
print("Test output:", TEST_ACTIVITY_FILE)

# Create the calendar of working days
working_days = pd.date_range(
    start=START_DATE,
    end=END_DATE,
    freq="B"
)

print("\nWORKING DAY CHECK")
print("Total working days:", len(working_days))
print("First working day:", working_days[0].date())
print("Last working day:", working_days[-1].date())

# Check whether weekends are excluded
weekends_present = (
    working_days.dayofweek >= 5
).any()

print("Weekends included:", weekends_present)

# Distribute 500 activities across 64 working days
base_activities = RECORDS_PER_DEVELOPER // len(working_days)

extra_activities = RECORDS_PER_DEVELOPER % len(working_days)

daily_activity_counts = np.full(
    len(working_days),
    base_activities,
    dtype=int
)

# Add one extra activity to the first days
daily_activity_counts[:extra_activities] += 1

print("\nDAILY ACTIVITY DISTRIBUTION")
print("Activities on a regular day:", base_activities)
print("Days receiving an extra activity:", extra_activities)
print("Days with 8 activities:", (daily_activity_counts == 8).sum())
print("Days with 7 activities:", (daily_activity_counts == 7).sum())
print("Total activities:", daily_activity_counts.sum())

# Activity types
activity_types = [
    "Coding",
    "Code_Review",
    "Debugging",
    "Testing",
    "Documentation",
    "Meeting",
]


def create_daily_schedule(work_date, activity_count):
    """Create a daily schedule that fits within 8 AM–6 PM."""

    work_start = pd.Timestamp(work_date).replace(
        hour=8, minute=0, second=0
    )
    work_end = pd.Timestamp(work_date).replace(
        hour=18, minute=0, second=0
    )

    # Breaks after every two activities, except the last
    break_count = (activity_count - 1) // 2
    break_minutes = break_count * 15

    available_minutes = (
        (work_end - work_start).total_seconds() / 60
        - break_minutes
    )

    # Ensure every activity gets at least 15 minutes
    if available_minutes < activity_count * 15:
        raise ValueError("Not enough working time for this day.")

    # Generate durations, then adjust them to fit the day
    durations = rng.integers(15, 61, size=activity_count)

    while durations.sum() > available_minutes:
        eligible = np.where(durations > 15)[0]

        if len(eligible) == 0:
            raise ValueError("Unable to fit activity durations.")

        index = int(rng.choice(eligible))
        durations[index] -= 1

    current_time = work_start
    daily_records = []

    for index, duration in enumerate(durations):
        # Break before the next pair of activities
        if index > 0 and index % 2 == 0:
            current_time += pd.Timedelta(minutes=15)

        activity_end = current_time + pd.Timedelta(
            minutes=int(duration)
        )

        daily_records.append({
            "timestamp": current_time,
            "activity_type": rng.choice(activity_types),
            "duration_minutes": int(duration),
        })

        current_time = activity_end

    return daily_records


# Test one working day
sample_date = working_days[0]
sample_count = int(daily_activity_counts[0])

sample_schedule = create_daily_schedule(
    sample_date,
    sample_count,
)

print("\nSINGLE-DAY SCHEDULE TEST")
print("Date:", sample_date.date())
print("Activities planned:", sample_count)

for activity in sample_schedule:
    start = activity["timestamp"]
    end = start + pd.Timedelta(
        minutes=activity["duration_minutes"]
    )

    print(
        f'{activity["activity_type"]} | '
        f'{start.strftime("%H:%M")}–{end.strftime("%H:%M")} | '
        f'{activity["duration_minutes"]} minutes'
    )

print("Activities created:", len(sample_schedule))

# Validate schedules across all working days
print("\nALL WORKING DAYS VALIDATION")

all_days_passed = True
total_test_activities = 0

for work_date, activity_count in zip(
    working_days,
    daily_activity_counts
):
    schedule = create_daily_schedule(
        work_date,
        int(activity_count),
    )

    total_test_activities += len(schedule)

    # Check the final activity's ending time
    final_activity = schedule[-1]

    final_end = (
        final_activity["timestamp"]
        + pd.Timedelta(
            minutes=final_activity["duration_minutes"]
        )
    )

    # Check for overlapping activities
    no_overlap = all(
        schedule[i]["timestamp"]
        + pd.Timedelta(
            minutes=schedule[i]["duration_minutes"]
        )
        <= schedule[i + 1]["timestamp"]
        for i in range(len(schedule) - 1)
    )

    within_workday = (
        schedule[0]["timestamp"].hour >= 8
        and final_end.hour < 18
        or (
            final_end.hour == 18
            and final_end.minute == 0
        )
    )

    if not no_overlap or not within_workday:
        all_days_passed = False
        print("Validation failed for:", work_date.date())

print("Working days tested:", len(working_days))
print("Expected activities:", RECORDS_PER_DEVELOPER)
print("Generated test activities:", total_test_activities)
print("All schedules valid:", all_days_passed)


# Generate schedules for all developers
print("\nFULL TEST DATASET GENERATION")

developers = pd.read_csv(DEVELOPER_FILE)
employee_ids = developers["employee_id"].tolist()

all_records = []

for employee_id in employee_ids:
    # Start with 7 activities on every working day
    employee_daily_counts = np.full(
        len(working_days),
        RECORDS_PER_DEVELOPER // len(working_days),
        dtype=int,
    )

    # Randomly select days for one extra activity
    extra_days = rng.choice(
        len(working_days),
        size=RECORDS_PER_DEVELOPER % len(working_days),
        replace=False,
    )

    employee_daily_counts[extra_days] += 1

    for work_date, activity_count in zip(
        working_days,
        employee_daily_counts,
    ):
        daily_schedule = create_daily_schedule(
            work_date,
            int(activity_count),
        )

        for activity in daily_schedule:
            all_records.append({
                "event_id": f"EVT{len(all_records) + 1:05d}",
                "employee_id": employee_id,
                "timestamp": activity["timestamp"],
                "activity_type": activity["activity_type"],
                "duration_minutes": activity["duration_minutes"],
                "is_simulated": True,
            })

# Convert records into a DataFrame
test_activities = pd.DataFrame(all_records)

print("Dataset shape:", test_activities.shape)
print("Unique developers:", test_activities["employee_id"].nunique())
print("Unique event IDs:", test_activities["event_id"].nunique())
print("Missing values:", test_activities.isna().sum().sum())

records_per_employee = test_activities.groupby(
    "employee_id"
).size()

print(
    "Exactly 500 records per developer:",
    records_per_employee.eq(RECORDS_PER_DEVELOPER).all()
)

# Save to the separate test file
test_activities.to_csv(TEST_ACTIVITY_FILE, index=False)

print("Test dataset saved to:", TEST_ACTIVITY_FILE)
print("Original dataset remains untouched.")



# Validate the complete test dataset
print("\nFINAL DATASET VALIDATION")

df = pd.read_csv(
    TEST_ACTIVITY_FILE,
    parse_dates=["timestamp"]
)

# 1. Check positive activity durations
positive_durations = (df["duration_minutes"] > 0).all()

# 2. Check that all timestamps fall on weekdays
weekdays_only = (df["timestamp"].dt.dayofweek < 5).all()

# 3. Check that activities start between 8 AM and 6 PM
start_minutes = (
    df["timestamp"].dt.hour * 60
    + df["timestamp"].dt.minute
)

valid_start_times = (
    (start_minutes >= 8 * 60)
    & (start_minutes < 18 * 60)
).all()

# 4. Check that activities finish by 6 PM
activity_end = (
    df["timestamp"]
    + pd.to_timedelta(df["duration_minutes"], unit="m")
)

end_of_workday = (
    df["timestamp"].dt.normalize()
    + pd.Timedelta(hours=18)
)

valid_end_times = (activity_end <= end_of_workday).all()

# 5. Check for overlapping activities per developer per day
overlap_found = False

df["_work_date"] = df["timestamp"].dt.date

for _, group in df.groupby(["employee_id", "_work_date"]):
    group = group.sort_values("timestamp")

    starts = group["timestamp"].reset_index(drop=True)
    ends = (
        group["timestamp"]
        + pd.to_timedelta(group["duration_minutes"], unit="m")
    ).reset_index(drop=True)

    if len(group) > 1 and (
        starts.iloc[1:].to_numpy()
        < ends.iloc[:-1].to_numpy()
    ).any():
        overlap_found = True
        break

# 6. Check record counts per developer
counts = df.groupby("employee_id").size()

correct_counts = counts.eq(RECORDS_PER_DEVELOPER).all()

# Display results
print("Total records:", len(df))
print("Positive durations:", positive_durations)
print("Weekdays only:", weekdays_only)
print("Valid start times:", valid_start_times)
print("Activities finish by 6 PM:", valid_end_times)
print("No overlapping activities:", not overlap_found)
print("500 records per developer:", correct_counts)

all_checks_passed = all([
    len(df) == TOTAL_ACTIVITY_RECORDS,
    positive_durations,
    weekdays_only,
    valid_start_times,
    valid_end_times,
    not overlap_found,
    correct_counts,
    df["employee_id"].nunique() == NUM_DEVELOPERS,
    df["event_id"].is_unique,
    df.isna().sum().sum() == 0,
])

print("ALL VALIDATION CHECKS PASSED:", all_checks_passed)

df.drop(columns=["_work_date"], inplace=True)