# CogniStream Dataset Design

## 1. Overview

CogniStream: Developer Flow-State & Cognitive Load Analytics is a data analytics project designed to explore simulated developer activity patterns, interruptions, focus indicators, cognitive-load proxies, and flow-state indicators.

The project uses Python to generate a structured synthetic dataset for exploratory data analysis and dashboard development.

## 2. Dataset Objectives

- Analyze developer activity patterns over time.
- Explore coding-session duration and task complexity.
- Examine interruption frequency and duration.
- Investigate context switching and its association with focus indicators.
- Explore relationships between task demands, cognitive-load proxies, and flow-state indicators.
- Prepare structured data for visualization and reporting.

## 3. Planned Dataset Specifications

| Specification | Planned value |
|---|---|
| Main activity records | 15,000 |
| Simulation period | 90 consecutive days |
| Fictional developer population | 30 |
| Main data format | CSV |
| Programming language | Python |
| Primary libraries | Pandas and NumPy |
| Reproducibility | Fixed random seed |

## 4. Planned Data Files

1. `cognistream_developers.csv` — fictional developer profiles.
2. `cognistream_activity.csv` — activity records and analytical indicators.
3. `cognistream_coding_sessions.csv` — coding-session information.
4. `cognistream_interruption_events.csv` — interruption-event information.

The files will be linked using identifiers such as `employee_id`, `event_id`, and `coding_session_id`, as applicable.

## 5. Main Activity Fields

The planned activity table includes event identifiers, developer identifiers, timestamps, activity types, project and tool information, programming languages, activity duration, coding-session references, interruption measures, context-switch measures, focus scores, cognitive-load proxies, flow-state proxies, task complexity, completion status, time features, and a synthetic-data indicator.

The final schema will be verified against the implemented generation code.

## 6. Data Generation Approach

Python will generate fictional developer profiles, activity events, coding sessions, and interruption events. Defined rules and probability distributions will be used to create realistic variation and logical relationships between records.

Focus, cognitive load, and flow state will be represented by simulated proxy scores. These indicators will be generated from documented assumptions rather than actual measurements of developers' mental states.

A fixed random seed will support reproducible generation.

## 7. Data Quality Requirements

The generated data will be checked for:

- Missing and duplicate records.
- Unique identifiers and valid relationships between files.
- Valid timestamps and durations.
- Consistent interruption and activity measures.
- Scores within their defined ranges.
- The expected record count and simulation period.

## 8. Limitations

This is a synthetic dataset, not a collection of real employee monitoring records. Its patterns depend on the assumptions and rules used in generation. Relationships observed in the dataset will not automatically establish causation or validate conclusions about real-world developers.

## 9. Project Status

**Current stage:** Synthetic developer profile and activity dataset generation.

Completed:
- Project folder structure and initial documentation.
- Synthetic developer profile generation.
- Fixed simulation configuration for 90 days.
- Generation of 15,000 synthetic activity records.
- Balanced distribution of 500 activity records per developer.
- Initial validation of record counts, identifiers, timestamps, and durations.

Next steps:
- Expand the activity schema with session, interruption, focus, cognitive-load, and flow-state indicators.
- Generate related coding-session and interruption-event datasets.
- Perform additional data quality checks and exploratory data analysis.
- Prepare the data for Power BI dashboard development.


## 10. Implementation Progress

### Developer Profile Generation

A Python script was created at `src/generate_dataset.py` to generate fictional developer profiles.

The script uses Pandas and NumPy to create a dataset containing developer identifiers, teams, experience levels, primary programming languages, and work schedules. An `is_simulated` field identifies the records as synthetic.

A fixed random seed is used to make the randomly generated attributes reproducible.

The generated output is saved as `data/raw/cognistream_developers.csv`.

### Dependencies

A `requirements.txt` file was created to record the Python package environment for reproducibility.


## 11. Activity Dataset Implementation

### Generated File

`data/raw/cognistream_activity.csv`

### Current Schema

| Column | Description |
|---|---|
| event_id | Unique identifier for each activity event |
| employee_id | Identifier linking the event to a developer profile |
| timestamp | Simulated activity start timestamp |
| activity_type | Type of developer activity |
| duration_minutes | Simulated activity duration |
| is_simulated | Indicates that the record is synthetic |

### Generation Rules

- Simulation period: January 1 to March 31, 2026, inclusive.
- Total records: 15,000.
- Developer population: 30 fictional developers.
- Activity records per developer: 500.
- Activity start times are generated between 08:00 and 18:00.
- Activity types include coding, code review, debugging, testing, documentation, and meetings.
- NumPy's seeded random-number generator is used for reproducible generation.

### Initial Validation

The generated dataset was checked for its total row count, unique event IDs, number of developers, per-developer record counts, and observed timestamp range.

All 15,000 event IDs are unique, all 30 developers have exactly 500 records each, and the observed timestamps fall within the planned simulation period.

### Current Limitations

The current activity dataset contains six columns. It does not yet include interruption events, context switching, coding-session identifiers, task complexity, focus scores, cognitive-load proxies, or flow-state indicators. These will be developed in subsequent stages.

The dataset is entirely synthetic and must not be interpreted as real employee monitoring data.
