
from datetime import date

# Simulation timeline
START_DATE = date(2026, 1, 1)
END_DATE = date(2026, 3, 31)

# Dataset size
NUM_DEVELOPERS = 30
TOTAL_ACTIVITY_RECORDS = 15_000

# Reproducibility
RANDOM_SEED = 42

# Derived settings
SIMULATION_DAYS = (END_DATE - START_DATE).days + 1

RECORDS_PER_DEVELOPER = (
    TOTAL_ACTIVITY_RECORDS // NUM_DEVELOPERS
)


# Display settings only when this file is run directly
if __name__ == "__main__":
    print("CogniStream configuration loaded")
    print(f"Simulation period: {START_DATE} to {END_DATE}")
    print(f"Simulation days: {SIMULATION_DAYS}")
    print(f"Developers: {NUM_DEVELOPERS}")
    print(f"Activity records: {TOTAL_ACTIVITY_RECORDS}")
    print(f"Records per developer: {RECORDS_PER_DEVELOPER}")

