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

**Current stage:** Dataset schema and project structure preparation.

The dataset has not yet been generated or validated. Those tasks will be completed in subsequent project stages.

## 10. Implementation Progress

### Developer Profile Generation

A Python script was created at `src/generate_dataset.py` to generate fictional developer profiles.

The script uses Pandas and NumPy to create a dataset containing developer identifiers, teams, experience levels, primary programming languages, and work schedules. An `is_simulated` field identifies the records as synthetic.

A fixed random seed is used to make the randomly generated attributes reproducible.

The generated output is saved as `data/raw/cognistream_developers.csv`.

### Dependencies

A `requirements.txt` file was created to record the Python package environment for reproducibility.
