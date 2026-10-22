from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/raw/cognistream_activity.csv"
OUTPUT = ROOT / "data/processed/daily_context_metrics.csv"

df = pd.read_csv(SOURCE)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["end_time"] = df["timestamp"] + pd.to_timedelta(
    df["duration_minutes"], unit="m"
)
df["work_date"] = df["timestamp"].dt.date
df = df.sort_values(["employee_id", "timestamp"])

results = []

for (employee, date), day in df.groupby(
    ["employee_id", "work_date"], sort=True
):
    day = day.sort_values("timestamp").reset_index(drop=True)

    context_switches = 0
    gaps = []

    for i in range(1, len(day)):
        previous = day.iloc[i - 1]
        current = day.iloc[i]

        if previous["activity_type"] != current["activity_type"]:
            context_switches += 1

        gap = (
            current["timestamp"] - previous["end_time"]
        ).total_seconds() / 60

        if gap >= 0:
            gaps.append(gap)

    long_gaps = [gap for gap in gaps if gap >= 5]

    results.append({
        "employee_id": employee,
        "work_date": str(date),
        "total_activities": len(day),
        "unique_activity_types": day["activity_type"].nunique(),
        "context_switches": context_switches,
        "meeting_count": int(
            (day["activity_type"] == "Meeting").sum()
        ),
        "gaps_5min_or_more": len(long_gaps),
        "minutes_in_gaps_5min_or_more": round(sum(long_gaps), 2),
        "longest_gap_minutes": round(max(gaps, default=0), 2),
        "total_activity_minutes": int(day["duration_minutes"].sum()),
        "is_simulated": True,
    })

result = pd.DataFrame(results)
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
result.to_csv(OUTPUT, index=False)

print("Day 6 context metrics created successfully.")
print(f"Daily records: {len(result)}")
print(f"Developers: {result['employee_id'].nunique()}")
print(f"Saved to: {OUTPUT.relative_to(ROOT)}")
