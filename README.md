# CogniStream — Developer Flow-State & Cognitive Load Analytics

## 1. Project Overview

### 1.1 Introduction

CogniStream is a data analytics project designed to explore developer work patterns, activity distribution, focus-session characteristics, interruptions, and context switching.

The project demonstrates how Python-based data generation, exploratory data analysis (EDA), statistical techniques, and Power BI visualisation can be combined to examine patterns in developer activity.

Using a synthetic dataset representing 30 fictional developers, the project investigates activity duration, focus-session metrics, daily work patterns, and differences across teams and experience levels.

The analytical findings are presented through an interactive, three-page Power BI dashboard.

**Important:** All records are synthetic. Focus and context-switching metrics are analytical proxies and do not directly measure actual productivity, cognitive load, attention, or mental states.

### 1.2 Problem Statement

Developer work involves multiple activities, interruptions, and changes in work context. Looking at activity counts alone may not provide sufficient insight into how work is distributed throughout a working day.

CogniStream addresses this analytical challenge by generating structured synthetic activity records and deriving daily developer metrics. It uses exploratory and multivariate analysis to investigate relationships among these indicators and presents the results through interactive visualisations.

### 1.3 Project Objectives

- Generate a structured synthetic dataset representing developer activity.
- Examine activity distribution and duration patterns.
- Analyse daily focus-session and context-switching indicators.
- Investigate relationships between activity and focus-related metrics.
- Compare activity patterns across teams and experience levels.
- Apply Principal Component Analysis (PCA) to explore underlying patterns.
- Develop an interactive Power BI dashboard.
- Communicate analytical findings and limitations through documentation.

## 2. Dataset Description

The project uses entirely synthetic data generated using Python, Pandas, and NumPy.

| Dataset | Records | Description |
|---|---:|---|
| Developer Profiles | 30 | Fictional developer information |
| Activity Events | 15,000 | Simulated developer activity records |
| Focus Sessions | 7,430 | Derived focus-session records |
| Daily Context Metrics | 1,920 | Daily context-switching indicators |
| Daily Developer Metrics | 1,920 | Integrated daily analytical metrics |

### Dataset Characteristics

- **Developers:** 30 fictional developers
- **Activity records:** 15,000
- **Records per developer:** 500
- **Simulation period:** January 1 – March 31, 2026
- **Working days:** 64
- **Activity categories:** Coding, Debugging, Testing, Documentation, Meeting, and Code Review

### Main Dataset Files

| File | Description |
|---|---|
| `data/raw/cognistream_developers.csv` | Synthetic developer profiles |
| `data/raw/cognistream_activity.csv` | Synthetic activity event records |
| `data/processed/focus_sessions.csv` | Derived focus-session records |
| `data/processed/daily_context_metrics.csv` | Daily context metrics |
| `data/processed/daily_developer_metrics.csv` | Integrated daily developer metrics |

## 3. Methodology

The project follows a structured data analytics workflow.

1. **Data Generation:** Created synthetic developer profiles and activity events using Python.
2. **Data Processing:** Generated focus-session records and daily context metrics.
3. **Data Integration:** Combined relevant indicators into a daily developer metrics dataset.
4. **Data Validation:** Checked record counts, missing values, duplicate records, and data consistency.
5. **Exploratory Data Analysis:** Examined distributions, summary statistics, and relationships between variables.
6. **Multivariate Analysis:** Applied Principal Component Analysis (PCA) to standardised numerical variables.
7. **Dashboard Development:** Created an interactive Power BI dashboard to communicate the analytical findings.

### EDA Sequence

The analysis followed three stages:

- **Univariate Analysis:** Examined individual variables and their distributions.
- **Bivariate Analysis:** Investigated relationships between pairs of numerical and categorical variables.
- **Multivariate Analysis:** Applied PCA to examine patterns across multiple variables simultaneously.

## 4. Key Analytical Findings

### 4.1 Univariate Analysis

- The average activity duration was approximately **37.39 minutes**.
- Developers recorded an average of approximately **7.81 activities per working day**.
- The average number of focus sessions was approximately **3.87 per day**.
- The average daily focus-session active time was approximately **243.34 minutes**.
- The average number of daily context switches was approximately **5.69**.

### 4.2 Bivariate Analysis

- Total focus-active minutes and average focus-session duration showed a strong positive correlation (approximately **0.899**).
- Average and longest focus-session durations also showed a positive relationship.
- Unique activity types and context switches showed a moderate positive correlation (approximately **0.465**).
- Mean activity duration was broadly similar across the six activity categories.

### 4.3 Multivariate Analysis — PCA

Principal Component Analysis was applied to seven standardised numerical variables.

- The first principal component explained approximately **48.3%** of the variance.
- The second principal component explained approximately **21.4%**.
- Together, the first two components explained approximately **69.7%** of the total variance.

PCA helped summarise patterns among related activity and focus-session indicators.

### 4.4 Important Interpretation

All findings describe the simulated dataset only. Correlations indicate statistical associations and do not establish cause-and-effect relationships.

For a detailed discussion, refer to [`documentation/key_insights.md`](documentation/key_insights.md).

## 5. Power BI Dashboard

The project includes an interactive three-page Power BI dashboard.

**Dashboard file:** [`CogniStream_Developer_Analytics_Dashboard.pbix`](CogniStream_Developer_Analytics_Dashboard.pbix)

### Page 1 — Overview

- Total activity records
- Total developers
- Average activity duration
- Average daily focus minutes
- Average daily context switches
- Activity distribution by category
- Average daily activity trend

### Page 2 — Activity & Focus Patterns

- Average activity duration by category
- Average daily focus minutes
- Average daily focus sessions by developer
- Average daily context switches by team

### Page 3 — Comparative Analysis

- Average daily activity minutes by team
- Average daily activity minutes by experience level
- Average daily focus minutes by team
- Interactive date slicer

## 6. Tools and Technologies

| Tool | Purpose |
|---|---|
| Python | Data generation and analysis |
| Pandas | Data manipulation and processing |
| NumPy | Numerical operations |
| Matplotlib | Data visualisation |
| Power BI Desktop | Interactive dashboard development |
| DAX | Dashboard measures |
| Git & GitHub | Version control and project management |
| GitHub Codespaces | Cloud-based development environment |

## 7. Limitations

- The project uses synthetic rather than real-world developer data.
- Focus-session and context-switching metrics are simulated or derived analytical proxies.
- The indicators cannot directly measure cognitive load, flow state, attention, or actual productivity.
- Correlations do not establish causation.
- Some metrics are mathematically related and should not be interpreted as independent indicators.
- Findings should not be generalised to real software development teams.

## 8. Conclusion

CogniStream demonstrates an end-to-end data analytics workflow, from synthetic data generation and processing to exploratory analysis, PCA, and interactive dashboard development.

The project highlights how structured data and analytical techniques can be used to investigate patterns in developer activity and work-related indicators.

It also demonstrates the importance of data validation, appropriate statistical interpretation, and transparent communication of analytical limitations.

## 9. Project Status

**Completed:** Synthetic data generation, data processing, exploratory data analysis, bivariate analysis, PCA, key insights documentation, and Power BI dashboard development.

---

*Developed as a Data Analytics Internship Project.*