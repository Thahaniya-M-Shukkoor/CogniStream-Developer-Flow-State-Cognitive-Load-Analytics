from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]

daily = pd.read_csv(ROOT / "data/processed/daily_developer_metrics.csv")
activity = pd.read_csv(ROOT / "data/raw/cognistream_activity.csv")
developers = pd.read_csv(ROOT / "data/raw/cognistream_developers.csv")

OUTPUT = ROOT / "data/processed"
FIGURES = ROOT / "reports/figures/univariate"
OUTPUT.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)

print("=" * 55)
print("DAY 9: CORRECTED UNIVARIATE ANALYSIS")
print("=" * 55)

def analyze_numeric(df, columns, name):
    data = df[columns].copy()
    summary = data.describe().T
    summary["missing_values"] = data.isna().sum()
    summary["unique_values"] = data.nunique()

    outliers = {}
    for col in columns:
        values = data[col].dropna()
        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        iqr = q3 - q1

        # Avoid misleading outlier flags when IQR is zero
        if iqr == 0:
            outliers[col] = "Not assessed (IQR = 0)"
        else:
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            outliers[col] = int(
                ((values < lower) | (values > upper)).sum()
            )

        plt.figure(figsize=(7, 4))
        plt.hist(values, bins="auto", edgecolor="black")
        plt.title(f"{name}: {col.replace('_', ' ').title()}")
        plt.xlabel(col.replace("_", " ").title())
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig(FIGURES / f"{name}_{col}_histogram.png", dpi=150)
        plt.close()

    summary["potential_outliers_iqr"] = pd.Series(outliers)
    summary.to_csv(OUTPUT / f"univariate_{name}_summary.csv")
    print(f"\n{name.upper()} NUMERICAL SUMMARY")
    print(summary.round(2).to_string())

activity_cols = ["duration_minutes"]
daily_cols = [
    "total_activities",
    "unique_activity_types",
    "context_switches",
    "meeting_count",
    "gaps_5min_or_more",
    "minutes_in_gaps_5min_or_more",
    "longest_gap_minutes",
    "total_activity_minutes",
    "focus_session_count",
    "total_focus_active_minutes",
    "average_focus_session_minutes",
    "longest_focus_session_minutes",
]

analyze_numeric(activity, activity_cols, "activity")
analyze_numeric(daily, daily_cols, "daily")

categorical = []
for column, df in [
    ("activity_type", activity),
    ("team", developers),
    ("experience_level", developers),
    ("primary_language", developers),
]:
    counts = df[column].value_counts(dropna=False)
    for category, count in counts.items():
        categorical.append({
            "variable": column,
            "category": str(category),
            "count": int(count),
            "percentage": round(count / len(df) * 100, 2),
        })

categorical_summary = pd.DataFrame(categorical)
categorical_summary.to_csv(
    OUTPUT / "univariate_categorical_summary.csv", index=False
)

print("\nCATEGORICAL DISTRIBUTIONS")
print(categorical_summary.to_string(index=False))

print("\nSOURCE DATA QUALITY")
for name, df in [
    ("Activity", activity),
    ("Daily", daily),
    ("Developers", developers),
]:
    print(f"{name}: {df.isna().sum().sum()} missing values")

print("\nCorrected univariate analysis completed.")
print("Numeric summaries saved separately for activity and daily data.")
print("Charts saved in reports/figures/univariate/")
