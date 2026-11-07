import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Paths
INPUT_FILE = "data/processed/daily_developer_metrics.csv"
OUTPUT_DIR = "data/processed"
FIGURE_DIR = "reports/figures/multivariate"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FIGURE_DIR, exist_ok=True)

# Load dataset
df = pd.read_csv(INPUT_FILE)

# Select meaningful numerical variables
features = [
    "unique_activity_types",
    "context_switches",
    "meeting_count",
    "total_activity_minutes",
    "total_focus_active_minutes",
    "average_focus_session_minutes",
    "longest_focus_session_minutes"
]

X = df[features].copy()

# Standardize variables
X_standardized = (X - X.mean()) / X.std(ddof=0)

# Perform PCA using Singular Value Decomposition
U, S, Vt = np.linalg.svd(X_standardized, full_matrices=False)

eigenvalues = (S ** 2) / (len(X) - 1)
explained_variance = eigenvalues / eigenvalues.sum()
cumulative_variance = np.cumsum(explained_variance)

# Calculate principal component scores
scores = U * S

# Save explained variance
variance_df = pd.DataFrame({
    "principal_component": [
        f"PC{i+1}" for i in range(len(features))
    ],
    "explained_variance_ratio": explained_variance,
    "cumulative_variance": cumulative_variance
})

variance_df.to_csv(
    f"{OUTPUT_DIR}/pca_explained_variance.csv", index=False
)

# Save component loadings
loadings = Vt.T * np.sqrt(eigenvalues)

loadings_df = pd.DataFrame(
    loadings,
    index=features,
    columns=[f"PC{i+1}" for i in range(len(features))]
)

loadings_df.to_csv(
    f"{OUTPUT_DIR}/pca_component_loadings.csv"
)

# Save PCA scores with developer information
scores_df = pd.DataFrame({
    "employee_id": df["employee_id"],
    "work_date": df["work_date"],
    "team": df["team"],
    "experience_level": df["experience_level"],
    "PC1": scores[:, 0],
    "PC2": scores[:, 1]
})

scores_df.to_csv(
    f"{OUTPUT_DIR}/pca_developer_scores.csv", index=False
)

# Group comparisons using PCA scores
group_summary = (
    scores_df.groupby(["team", "experience_level"])[["PC1", "PC2"]]
    .agg(["mean", "median", "std"])
)

group_summary.to_csv(
    f"{OUTPUT_DIR}/pca_group_summary.csv"
)

# Plot 1: Explained variance
plt.figure(figsize=(9, 5))
plt.bar(variance_df["principal_component"],
        variance_df["explained_variance_ratio"])
plt.plot(variance_df["principal_component"],
         variance_df["cumulative_variance"], marker="o")
plt.xlabel("Principal Components")
plt.ylabel("Variance Explained")
plt.title("PCA Explained and Cumulative Variance")
plt.tight_layout()
plt.savefig(f"{FIGURE_DIR}/pca_explained_variance.png", dpi=300)
plt.close()

# Plot 2: PCA scores by team
plt.figure(figsize=(9, 6))
for team, group in scores_df.groupby("team"):
    plt.scatter(group["PC1"], group["PC2"], label=team, alpha=0.6)

plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("PCA Scores by Developer Team")
plt.legend()
plt.tight_layout()
plt.savefig(f"{FIGURE_DIR}/pca_scores_by_team.png", dpi=300)
plt.close()

# Plot 3: PCA scores by experience level
plt.figure(figsize=(9, 6))
for level, group in scores_df.groupby("experience_level"):
    plt.scatter(group["PC1"], group["PC2"], label=level, alpha=0.6)

plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("PCA Scores by Experience Level")
plt.legend()
plt.tight_layout()
plt.savefig(f"{FIGURE_DIR}/pca_scores_by_experience.png", dpi=300)
plt.close()

# Plot 4: Component loadings
plt.figure(figsize=(10, 6))
loadings_df[["PC1", "PC2"]].plot(
    kind="bar", figsize=(10, 6)
)
plt.ylabel("Component Loading")
plt.title("Variable Contributions to the First Two Components")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(f"{FIGURE_DIR}/pca_component_loadings.png", dpi=300)
plt.close()

print("\nMULTIVARIATE ANALYSIS COMPLETED")
print("\nExplained variance:")
print(variance_df.round(3).to_string(index=False))

print("\nComponent loadings:")
print(loadings_df[["PC1", "PC2"]].round(3))

print("\nGenerated CSV files:")
print(" - pca_explained_variance.csv")
print(" - pca_component_loadings.csv")
print(" - pca_developer_scores.csv")
print(" - pca_group_summary.csv")

print("\nGenerated visualizations:")
print(os.listdir(FIGURE_DIR))
