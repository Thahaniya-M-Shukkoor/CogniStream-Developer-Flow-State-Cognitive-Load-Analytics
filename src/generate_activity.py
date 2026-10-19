
import sys
from pathlib import Path

import pandas as pd
import numpy as np

# Identify the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Make the project root available for imports
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import (
    START_DATE,
    END_DATE,
    NUM_DEVELOPERS,
    TOTAL_ACTIVITY_RECORDS,
    RECORDS_PER_DEVELOPER,
    RANDOM_SEED,
)

# Make random generation reproducible
rng = np.random.default_rng(RANDOM_SEED)

# Define data paths
DATA_DIR = PROJECT_ROOT / "data" / "raw"

DEVELOPER_FILE = DATA_DIR / "cognistream_developers.csv"
ACTIVITY_FILE = DATA_DIR / "cognistream_activity.csv"

print("CogniStream activity generator initialized")
print(f"Developer file exists: {DEVELOPER_FILE.exists()}")
print(f"Target activity records: {TOTAL_ACTIVITY_RECORDS}")
print(f"Records per developer: {RECORDS_PER_DEVELOPER}")
print(f"Simulation period: {START_DATE} to {END_DATE}")

# Load the existing developer profiles
developers = pd.read_csv(DEVELOPER_FILE)

# Extract the employee IDs
employee_ids = developers["employee_id"].tolist()

# Display a summary
print("\nDeveloper profiles loaded successfully!")
print("Number of developer profiles:", len(developers))
print("Number of employee IDs:", len(employee_ids))
print("First five employee IDs:", employee_ids[:5])
print("All employee IDs unique:", developers["employee_id"].is_unique)


# Activity types that developers may perform
activity_types = [
    "Coding",
    "Code_Review",
    "Debugging",
    "Testing",
    "Documentation",
    "Meeting",
]

# Generate exactly 500 records per developer
records = []

for employee_id in employee_ids:
    for _ in range(RECORDS_PER_DEVELOPER):
        random_day = rng.integers(
            0,
            (END_DATE - START_DATE).days + 1
        )

        timestamp = (
            pd.Timestamp(START_DATE)
            + pd.Timedelta(days=int(random_day))
            + pd.Timedelta(
                minutes=int(rng.integers(8 * 60, 18 * 60))
            )
        )

        records.append({
            "event_id": f"EVT{len(records) + 1:05d}",
            "employee_id": employee_id,
            "timestamp": timestamp,
            "activity_type": rng.choice(activity_types),
            "duration_minutes": int(rng.integers(5, 121)),
            "is_simulated": True,
        })

# Convert the records into a DataFrame
activities = pd.DataFrame(records)

# Save the complete activity dataset
activities.to_csv(ACTIVITY_FILE, index=False)

print("\nActivity dataset generated successfully!")
print("Dataset shape:", activities.shape)
print("Saved to:", ACTIVITY_FILE)

