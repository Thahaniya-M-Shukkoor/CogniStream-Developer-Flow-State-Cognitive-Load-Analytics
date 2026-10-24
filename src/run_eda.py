from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

DAILY_FILE = ROOT / "data/processed/daily_developer_metrics.csv"
ACTIVITY_FILE = ROOT / "data/raw/cognistream_activity.csv"
OUTPUT_DIR = ROOT / "data/processed"

daily = pd.read_csv(DAILY_FILE)
activity = pd.read_csv(ACTIVITY_FILE)

print("=" * 55)
print("COGNISTREAM - DAY 8 EXPLORATORY DATA ANALYSIS")
print("=" * 55)

# 1. Dataset overview
print("\n1. DATASET OVERVIEW")
print(f"Daily dataset shape: {daily.shape}")
print(f"Activity dataset shape: {activity.shape}")
print(f"Unique developers: {daily['employee_id'].nunique()}")
print(f"Working dates: {daily['work_date'].nunique()}")
print(f"Missing values in daily dataset: {daily.isna().sum().sum()}")
print(
    "Duplicate developer-days:",
    daily.duplicated(["employee_id", "work_date"]).sum()
)

# 2. Activity type distribution
print("\n2. ACTIVITY TYPE DISTRIBUTION")
activity_summary = (
    activity.groupby("activity_type")
    .agg(
        activity_count=("event_id", "count"),
        average_duration_minutes=("duration_minutes", "mean"),
        total_duration_minutes=("duration_minutes", "sum"),
    )
    .reset_index()
    .sort_values("activity_count", ascending=False)
)

activity_summary["average_duration_minutes"] = (
    activity_summary["average_duration_minutes"].round(2)
)
print(activity_summary.to_string(index=False))

# 3. Daily metrics overview
print("\n3. DAILY METRICS - DESCRIPTIVE STATISTICS")
metrics = [
    "total_activities",
    "unique_activity_types",
    "context_switches",
    "meeting_count",
    "total_activity_minutes",
    "focus_session_count",
    "total_focus_active_minutes",
    "average_focus_session_minutes",
]

print(daily[metrics].describe().round(2).to_string())

# 4. Compare daily averages across teams
print("\n4. TEAM-LEVEL COMPARISON")
team_summary = (
    daily.groupby("team")
    .agg(
        developer_count=("employee_id", "nunique"),
        avg_daily_activities=("total_activities", "mean"),
        avg_context_switches=("context_switches", "mean"),
        avg_meetings=("meeting_count", "mean"),
        avg_focus_sessions=("focus_session_count", "mean"),
        avg_focus_active_minutes=("total_focus_active_minutes", "mean"),
    )
    .reset_index()
    .round(2)
)

print(team_summary.to_string(index=False))

# Save reusable summary tables
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
activity_summary.to_csv(
    OUTPUT_DIR / "eda_activity_summary.csv", index=False
)
team_summary.to_csv(
    OUTPUT_DIR / "eda_team_summary.csv", index=False
)

print("\n5. OUTPUT FILES")
print("Saved: data/processed/eda_activity_summary.csv")
print("Saved: data/processed/eda_team_summary.csv")
print("\nDay 8 initial EDA completed successfully.")
