
import pandas as pd
import numpy as np
from pathlib import Path

# Set a fixed random seed for reproducibility
np.random.seed(42)

# Define the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Create the output folder if it does not exist
DATA_DIR = PROJECT_ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Define fictional developer profiles
num_developers = 30

employee_ids = [
    f"EMP{i:03d}" for i in range(1, num_developers + 1)
]

teams = np.random.choice(
    ["Backend", "Frontend", "Data", "QA", "DevOps"],
    size=num_developers
)

experience_levels = np.random.choice(
    ["Beginner", "Intermediate", "Advanced"],
    size=num_developers,
    p=[0.30, 0.50, 0.20]
)

programming_languages = np.random.choice(
    ["Python", "JavaScript", "Java", "SQL", "C#"],
    size=num_developers
)

work_schedules = np.random.choice(
    ["Standard", "Flexible"],
    size=num_developers,
    p=[0.70, 0.30]
)

# Create a DataFrame from the generated information
developers = pd.DataFrame({
    "employee_id": employee_ids,
    "team": teams,
    "experience_level": experience_levels,
    "primary_language": programming_languages,
    "work_schedule": work_schedules,
    "is_simulated": True
})

# Save the developer profiles to a CSV file
output_file = DATA_DIR / "cognistream_developers.csv"
developers.to_csv(output_file, index=False)

# Display a summary
print("Developer dataset created successfully!")
print(f"Number of developers: {len(developers)}")
print(f"Saved to: {output_file}")
print("\nFirst five developer profiles:")
print(developers.head())
