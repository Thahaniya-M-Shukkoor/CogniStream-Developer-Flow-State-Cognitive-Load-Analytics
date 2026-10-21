from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/raw/cognistream_activity.csv"
OUTPUT = ROOT / "data/processed/focus_sessions.csv"

df = pd.read_csv(SOURCE)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["end_time"] = df["timestamp"] + pd.to_timedelta(
    df["duration_minutes"], unit="m"
)
df["work_date"] = df["timestamp"].dt.date
df = df.sort_values(["employee_id", "timestamp"])

sessions = []

for (employee, work_date), day in df.groupby(
    ["employee_id", "work_date"], sort=True
):
    current = []

    def save_session(events):
        if not events:
            return

        start = events[0]["timestamp"]
        end = events[-1]["end_time"]
        active_minutes = sum(e["duration_minutes"] for e in events)

        sessions.append({
            "employee_id": employee,
            "work_date": str(work_date),
            "session_start": start,
            "session_end": end,
            "activity_count": len(events),
            "active_minutes": active_minutes,
            "elapsed_minutes": int((end - start).total_seconds() / 60),
            "gap_minutes": int((end - start).total_seconds() / 60)
                           - active_minutes,
            "activity_types": ", ".join(
                sorted({e["activity_type"] for e in events})
            ),
            "source_event_ids": ", ".join(
                e["event_id"] for e in events
            ),
            "is_simulated": True,
            "session_definition":
                "Consecutive non-meeting activities with no gap",
        })

    for row in day.to_dict("records"):
        if row["activity_type"] == "Meeting":
            save_session(current)
            current = []
            continue

        if current:
            previous_end = current[-1]["end_time"]
            gap = (row["timestamp"] - previous_end).total_seconds() / 60

            if gap > 1:
                save_session(current)
                current = []

        current.append(row)

    save_session(current)

result = pd.DataFrame(sessions)

if result.empty:
    raise ValueError("No focus sessions were generated.")

result.insert(
    0, "session_id",
    [f"FS{i:05d}" for i in range(1, len(result) + 1)]
)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
result.to_csv(OUTPUT, index=False)

print("Focus-session dataset created successfully.")
print(f"Sessions: {len(result)}")
print(f"Developers: {result['employee_id'].nunique()}")
print(f"Saved to: {OUTPUT.relative_to(ROOT)}")
