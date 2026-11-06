# DAY 10: BIVARIATE ANALYSIS
# CogniStream - Developer Flow-State & Cognitive Load Analytics

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# 1. LOAD DATASETS
# --------------------------------------------------

daily_df = pd.read_csv("data/processed/daily_developer_metrics.csv")
activity_df = pd.read_csv("data/raw/cognistream_activity.csv")

os.makedirs("reports/figures/bivariate", exist_ok=True)

print("=" * 55)
print("DAY 10: BIVARIATE ANALYSIS")
print("=" * 55)

print("\nDaily dataset shape:", daily_df.shape)
print("Activity dataset shape:", activity_df.shape)


# --------------------------------------------------
# 2. NUMERICAL VS NUMERICAL
# --------------------------------------------------

numeric_columns = [
    "total_activities",
    "unique_activity_types",
    "context_switches",
    "meeting_count",
    "total_activity_minutes",
    "focus_session_count",
    "total_focus_active_minutes",
    "average_focus_session_minutes",
    "longest_focus_session_minutes"
]

numeric_df = daily_df[numeric_columns]

# Pearson correlation
pearson_corr = numeric_df.corr(method="pearson")

# Spearman correlation
spearman_corr = numeric_df.corr(method="spearman")

# Save correlation matrices
pearson_corr.to_csv(
    "data/processed/bivariate_pearson_correlation.csv"
)

spearman_corr.to_csv(
    "data/processed/bivariate_spearman_correlation.csv"
)

# Save unique correlation pairs
correlation_results = []

for i in range(len(numeric_columns)):
    for j in range(i + 1, len(numeric_columns)):
        correlation_results.append({
            "variable_1": numeric_columns[i],
            "variable_2": numeric_columns[j],
            "pearson_correlation": pearson_corr.iloc[i, j],
            "spearman_correlation": spearman_corr.iloc[i, j]
        })

correlation_df = pd.DataFrame(correlation_results)

correlation_df.to_csv(
    "data/processed/bivariate_correlation_summary.csv",
    index=False
)

print("\nTop positive Pearson correlations:")
print(
    correlation_df.sort_values(
        "pearson_correlation", ascending=False
    ).head(10).to_string(index=False)
)


# --------------------------------------------------
# 3. CORRELATION HEATMAP
# --------------------------------------------------

plt.figure(figsize=(12, 9))

plt.imshow(
    pearson_corr,
    cmap="coolwarm",
    vmin=-1,
    vmax=1
)

plt.colorbar(label="Pearson Correlation")

plt.xticks(
    range(len(numeric_columns)),
    numeric_columns,
    rotation=45,
    ha="right"
)

plt.yticks(
    range(len(numeric_columns)),
    numeric_columns
)

for i in range(len(numeric_columns)):
    for j in range(len(numeric_columns)):
        value = pearson_corr.iloc[i, j]
        if pd.notna(value):
            plt.text(
                j, i, f"{value:.2f}",
                ha="center", va="center", fontsize=8
            )

plt.title("Bivariate Analysis - Correlation Heatmap")
plt.tight_layout()

plt.savefig(
    "reports/figures/bivariate/correlation_heatmap.png",
    dpi=300
)

plt.close()


# --------------------------------------------------
# 4. SELECTED SCATTER PLOTS
# --------------------------------------------------

selected_pairs = [
    ("context_switches", "average_focus_session_minutes"),
    ("meeting_count", "focus_session_count"),
    ("total_activities", "total_focus_active_minutes"),
    ("total_activity_minutes", "total_focus_active_minutes")
]

for x_col, y_col in selected_pairs:

    plt.figure(figsize=(8, 5))

    plt.scatter(
        daily_df[x_col],
        daily_df[y_col],
        alpha=0.4
    )

    plt.xlabel(x_col.replace("_", " ").title())
    plt.ylabel(y_col.replace("_", " ").title())
    plt.title(f"{x_col} vs {y_col}")

    plt.tight_layout()

    filename = f"{x_col}_vs_{y_col}.png"

    plt.savefig(
        f"reports/figures/bivariate/{filename}",
        dpi=300
    )

    plt.close()


# --------------------------------------------------
# 5. CATEGORICAL VS NUMERICAL
# --------------------------------------------------

group_results = []

group_columns = ["team", "experience_level"]

metrics = [
    "total_activity_minutes",
    "context_switches",
    "focus_session_count",
    "average_focus_session_minutes"
]

for group_col in group_columns:

    for group_value, group_data in daily_df.groupby(group_col):

        for metric in metrics:

            group_results.append({
                "grouping_variable": group_col,
                "group_value": group_value,
                "metric": metric,
                "count": group_data[metric].count(),
                "mean": group_data[metric].mean(),
                "median": group_data[metric].median(),
                "std": group_data[metric].std()
            })

group_summary = pd.DataFrame(group_results)

group_summary.to_csv(
    "data/processed/bivariate_group_summary.csv",
    index=False
)

# Comparison charts by team and experience level
for group_col in group_columns:

    for metric in metrics:

        plt.figure(figsize=(9, 5))

        daily_df.boxplot(
            column=metric,
            by=group_col,
            grid=False
        )

        plt.title(
            f"{metric.replace('_', ' ').title()} by "
            f"{group_col.replace('_', ' ').title()}"
        )

        plt.suptitle("")
        plt.xlabel(group_col.replace("_", " ").title())
        plt.ylabel(metric.replace("_", " ").title())

        plt.tight_layout()

        plt.savefig(
            f"reports/figures/bivariate/"
            f"{metric}_by_{group_col}.png",
            dpi=300
        )

        plt.close()

# --------------------------------------------------
# 6. ACTIVITY TYPE VS ACTIVITY DURATION
# --------------------------------------------------

activity_summary = activity_df.groupby(
    "activity_type"
)["duration_minutes"].agg(
    ["count", "mean", "median", "std", "min", "max"]
).reset_index()

activity_summary.to_csv(
    "data/processed/bivariate_activity_summary.csv",
    index=False
)

plt.figure(figsize=(10, 6))

activity_df.boxplot(
    column="duration_minutes",
    by="activity_type",
    grid=False
)

plt.title("Activity Duration by Activity Type")
plt.suptitle("")
plt.xlabel("Activity Type")
plt.ylabel("Duration (Minutes)")
plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    "reports/figures/bivariate/activity_duration_by_type.png",
    dpi=300
)

plt.close()


# --------------------------------------------------
# 7. FINAL SUMMARY
# --------------------------------------------------

print("\nActivity duration by type:")
print(activity_summary.to_string(index=False))

print("\nTeam and experience-level comparisons:")
print(group_summary.to_string(index=False))

print("\nBivariate analysis completed successfully!")

print("\nGenerated files:")
print("- Pearson and Spearman correlation matrices")
print("- Bivariate correlation summary")
print("- Bivariate group summary")
print("- Bivariate activity summary")
print("- Visualizations in reports/figures/bivariate/")