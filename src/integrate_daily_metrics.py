from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

DEVELOPERS = ROOT / "data/raw/cognistream_developers.csv"
CONTEXT = ROOT / "data/processed/daily_context_metrics.csv"
FOCUS = ROOT / "data/processed/focus_sessions.csv"
OUTPUT = ROOT / "data/processed/daily_developer_metrics.csv"

developers = pd.read_csv(DEVELOPERS)
context = pd.read_csv(CONTEXT)
focus = pd.read_csv(FOCUS)

# Standardize dates for reliable merging
context["work_date"] = pd.to_datetime(context["work_date"]).dt.strftime("%Y-%m-%d")
focus["work_date"] = pd.to_datetime(focus["work_date"]).dt.strftime("%Y-%m-%d")

# Summarize focus sessions for each developer on each working day
focus_daily = (
    focus.groupby(["employee_id", "work_date"])
    .agg(
        focus_session_count=("session_id", "count"),
        total_focus_active_minutes=("active_minutes", "sum"),
        average_focus_session_minutes=("active_minutes", "mean"),
        longest_focus_session_minutes=("active_minutes", "max"),
        total_focus_elapsed_minutes=("elapsed_minutes", "sum"),
    )
    .reset_index()
)

# Add developer profile information to the daily context records
profile_columns = [
    "employee_id",
    "team",
    "experience_level",
    "primary_language",
    "work_schedule",
]

daily = context.merge(
    developers[profile_columns],
    on="employee_id",
    how="left",
    validate="many_to_one",
)

# Add the daily focus-session summaries
daily = daily.merge(
    focus_daily,
    on=["employee_id", "work_date"],
    how="left",
    validate="one_to_one",
)

# A zero means no focus session was recorded for that developer-day
focus_columns = [
    "focus_session_count",
    "total_focus_active_minutes",
    "average_focus_session_minutes",
    "longest_focus_session_minutes",
    "total_focus_elapsed_minutes",
]
daily[focus_columns] = daily[focus_columns].fillna(0).round(2)

# Validate the integrated dataset
assert len(daily) == len(context), "Daily row count changed unexpectedly."
assert not daily.duplicated(["employee_id", "work_date"]).any(), \
    "Duplicate developer-day records found."
assert daily["team"].notna().all(), "Some developer profiles did not match."
assert daily["is_simulated"].all(), "Unexpected non-simulated records found."

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
daily.to_csv(OUTPUT, index=False)

print("Day 7 integration completed successfully!")
print(f"Output: {OUTPUT.relative_to(ROOT)}")
print(f"Shape: {daily.shape}")
print(f"Unique developers: {daily['employee_id'].nunique()}")
print(f"Unique working dates: {daily['work_date'].nunique()}")
print(f"Duplicate developer-day records: {daily.duplicated(['employee_id', 'work_date']).sum()}")
print(f"Missing values: {daily.isna().sum().sum()}")
print("All validation checks passed.")
