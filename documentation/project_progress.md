# CogniStream — Project Development Progress

## 1. Project Development Overview

CogniStream is a synthetic data analytics project developed to explore developer activity patterns, focus-session indicators, context switching, and activity-based cognitive-load proxies.

The project uses Python, Pandas, and NumPy for data generation, processing, and exploratory data analysis. The generated datasets represent fictional developers and simulated activity patterns.

The project follows a structured analytical workflow:

1. Data generation
2. Data validation and preprocessing
3. Dataset integration
4. Univariate analysis
5. Bivariate analysis
6. Multivariate analysis
7. Insights and dashboard development

---

## 2. Development Progress
### 2.1 — Project Initialization

- Established the CogniStream project concept and objectives.
- Created the initial project structure.
- Identified the major stages of the project, including synthetic data generation, analysis, and visualization.

### 2.2 — Developer Profile Generation

**Script:** `src/generate_dataset.py`

**Output:** `data/raw/cognistream_developers.csv`

Generated profiles for 30 fictional developers.

The dataset includes:

- `employee_id`
- `team`
- `experience_level`
- `primary_language`
- `work_schedule`
- `is_simulated`

The dataset establishes the developer identifiers used to connect activity records with developer profiles.

### 2.3 — Initial Activity Dataset Generation

**Script:** `src/generate_activity.py`

**Output:** `data/raw/cognistream_activity.csv`

Generated 15,000 synthetic developer activity records.

The dataset includes six activity types:

- Coding
- Code Review
- Debugging
- Testing
- Documentation
- Meeting

Initial validation confirmed 15,000 records, 30 developers, and 500 records per developer.

### 2.4 — Workday-Based Activity Scheduling

**Script:** `src/generate_workday_activity.py`

Improved the activity generation process by introducing workday-based scheduling.

Key specifications:

- Simulation period: January 1 to March 31, 2026.
- Total records: 15,000.
- Developers: 30.
- Records per developer: 500.
- Working days: 64.
- Activity start times restricted to the planned working-hour window.
- Weekend activity generation excluded.

The activity dataset was regenerated using the revised scheduling logic.

Validation confirmed the expected record count, developer distribution, and absence of missing values.

### 2.5 — Focus Session Generation

**Script:** `src/generate_focus_sessions.py`

**Output:** `data/processed/focus_sessions.csv`

Generated a separate focus-session dataset from the activity records.

The resulting dataset contains:

- 7,430 simulated focus sessions.
- Records associated with all 30 developers.
- Session-level duration and activity information.

These sessions provide activity-based indicators for examining sustained periods of developer work. They are simulated proxies and do not represent directly measured concentration or mental focus.

### 2.6 — Daily Context Metrics Generation

**Script:** `src/generate_context_metrics.py`

**Output:** `data/processed/daily_context_metrics.csv`

Generated daily context metrics for the developer population.

The dataset contains 1,920 records, representing 30 developers across 64 working days.

It provides daily measures related to activity patterns, context switching, and meeting activity.

### 2.7 — Daily Metrics Integration

**Script:** `src/integrate_daily_metrics.py`

**Output:** `data/processed/daily_developer_metrics.csv`

Integrated the generated daily activity, focus-session, and context metrics into a consolidated developer-day dataset.

**Validation results:**

- Records: 1,920
- Columns: 20
- Developers: 30
- Working dates: 64
- Duplicate developer-day records: 0
- Missing values: 0

The integrated dataset provides the main analytical foundation for subsequent exploratory data analysis.

### 2.8 — Initial Exploratory Data Analysis

**Script:** `src/run_eda.py`

Initial exploratory data analysis was conducted to understand the structure and distribution of the generated datasets.

**Outputs:**

- `data/processed/eda_activity_summary.csv`
- `data/processed/eda_team_summary.csv`

The analysis examined:

- Dataset dimensions and structure.
- Developer and activity distributions.
- Daily activity patterns.
- Context-switching metrics.
- Focus-session metrics.
- Team-level descriptive summaries.

The analysis confirmed that the integrated daily dataset contained 1,920 developer-day records with no missing values or duplicate developer-day combinations.

### 2.9 — Univariate Analysis

**Script:** `src/univariate_analysis.py`

Conducted univariate analysis to examine individual variables independently before investigating relationships between variables.

**Outputs:**

- `data/processed/univariate_activity_summary.csv`
- `data/processed/univariate_daily_summary.csv`
- `data/processed/univariate_categorical_summary.csv`
- `reports/figures/univariate/`

The analysis covered numerical and categorical variables from the activity and daily developer datasets.

**Key descriptive findings:**

| Metric | Result |
|---|---:|
| Average activity duration | 37.39 minutes |
| Minimum activity duration | 15 minutes |
| Maximum activity duration | 60 minutes |
| Average daily activities | 7.81 |
| Average unique activity types per day | 4.57 |
| Average context switches per day | 5.69 |
| Average meeting count per day | 1.31 |
| Average focus sessions per day | 3.87 |
| Average focus-session duration | 62.90 minutes |

The categorical analysis also examined the distribution of activity types, developer teams, experience levels, and programming languages.

**Important observations and limitations:**

- Activity durations ranged from 15 to 60 minutes.
- Daily activity counts ranged from 7 to 8.
- The generated data showed a relatively balanced distribution of activity types.
- Some gap-related metrics were constant because of the predefined scheduling rules.
- These constant metrics should not be treated as meaningful indicators for comparing developers.
- The dataset is synthetic, and all findings describe the generated data rather than actual developer behaviour.

---

## 3. Current Project Structure

The main project components developed so far include:

| Folder | Purpose |
|---|---|
| `data/raw/` | Original synthetic developer and activity datasets |
| `data/processed/` | Generated focus sessions, daily metrics, and analysis outputs |
| `src/` | Python scripts for generation, integration, and analysis |
| `documentation/` | Dataset design and project documentation |
| `reports/figures/` | Visual outputs from exploratory analysis |

---

## 4. Current Project Status

**Completed:**

- Project initialization and dataset planning.
- Synthetic developer profile generation.
- Activity dataset generation and workday scheduling.
- Focus-session generation.
- Daily context metrics generation.
- Integration of daily developer metrics.
- Initial exploratory data analysis.
- Univariate analysis and visualizations.

**Upcoming work:**

1. Bivariate analysis to investigate relationships between selected variables.
2. Multivariate analysis to examine combinations of variables.
3. Interpretation of analytical findings and identification of meaningful patterns.
4. Preparation of insights and recommendations.
5. Development of a Power BI dashboard.

---

## 5. Overall Data Limitations

CogniStream uses entirely synthetic data generated through predefined assumptions and probability-based rules.

Focus sessions, context switching, and other activity measures are analytical proxies. They do not directly measure developers' psychological states, productivity, or actual cognitive load.

The findings are useful for demonstrating data analytics workflows and exploring simulated patterns. They should not be generalized to real-world developers without validation using appropriate real-world data.