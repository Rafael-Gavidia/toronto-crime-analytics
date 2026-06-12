# Toronto Crime Indicators Analytics Tool

A data analytics dashboard built with Python and Streamlit for exploring and visualizing crime indicators in Toronto using the Toronto Crime Indicators dataset.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Team](#team)
- [Project Management](#project-management)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Running the Dashboard](#running-the-dashboard)
- [Running Tests](#running-tests)
- [Dataset](#dataset)
- [Features](#features)

---

## Project Overview

This tool was built as a final group project applying Agile practices across two sprints. It allows users to load, clean, and interactively explore Toronto crime data through a multi-page Streamlit dashboard, with analytics covering crime trends, neighbourhood breakdowns, offence distributions, division performance, and more.

---

## Team

| Name | GitHub |
|------|--------|
| *Gulbanu Mukhanbetkali* | `@Banu_mgm` |
| *Kyungsun Choi* | `@Sunida83-maker` |
| *Simran Kaur* | `@SimranKaur759` |
| *Rafael Gavidia* | `@Rafael-Gavidia` |

---

## Project Management

- **GitHub Repository:** *https://github.com/Rafael-Gavidia/toronto-crime-analytics*
- **Taiga Project:** *https://tree.taiga.io/project/sunida83-maker-toronto-crime-indicators-analytics-tool/timeline*

---

## Tech Stack

- Python 3.11+
- Streamlit
- Pandas
- Plotly
- Pytest

---

## Project Structure

```
toronto-crime-analytics/
├── app.py                        # Streamlit dashboard entry point
├── main.py                       # CLI entry point for running analytics
├── make_sample.py                # Script for generating sample data
├── requirements.txt
├── pytest.ini
├── .gitignore
├── README.md
│
├── data/
│   └── Toronto_Crime_Indicators.csv
│
└── src/
│   ├── __init__.py
│   ├── data_loader.py            # Load raw CSV data
│   ├── cleaner.py                # Data cleaning and validation
│   ├── pipeline.py               # Full load + clean pipeline
│   ├── crime_by_hour.py          # Crimes by hour of day analysis
│   ├── neighbourhood.py          # Neighbourhood-level analysis
│   ├── offence_distribution.py   # Offence type breakdown
│   ├── trends.py                 # Crime trends over time
│   ├── division.py               # Police division data
│   ├── division_performance.py   # Division performance metrics
│   └── premises.py               # Premises type analysis
│
└── tests/
    ├── test_data_loader.py
    ├── test_cleaner.py
    ├── test_pipeline.py
    ├── test_crime_by_hour.py
    ├── test_neighbourhood.py
    ├── test_offence_distribution.py
    ├── test_trends.py
    ├── test_division.py
    ├── test_division_performance.py
    ├── test_premises.py
    └── test_dashboard.py
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-org>/toronto-crime-analytics.git
cd toronto-crime-analytics
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the dataset

Place the `Toronto_Crime_Indicators.csv` file inside the `data/` folder:

```
data/Toronto_Crime_Indicators.csv
```

> The dataset is not included in this repository. Obtain it from the course materials.

---

## Running the Dashboard

```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`.

Use the sidebar to navigate between views:

- **Overview** — key summary metrics
- **Crime by Hour** — hourly distribution of incidents
- **Neighbourhood Analysis** — crime counts by neighbourhood
- **Offence Distribution** — breakdown by offence type
- **Crime Trends** — incidents over time
- **Division Performance** — activity by police division
- **Premises Analysis** — breakdown by premises type

---

## Running Tests

```bash
pytest
```

To run with verbose output:

```bash
pytest -v
```

Tests are located in the `tests/` folder. Five user stories were implemented using full TDD (Red → Green → Refactor).

---

## Dataset

**Source:** Toronto Crime Indicators (provided via course materials)

The dataset includes records of major crime incidents in Toronto with the following key fields:

| Field | Description |
|-------|-------------|
| `OCC_DATE` | Date of occurrence |
| `REPORT_DATE` | Date the crime was reported |
| `OFFENCE` | Type of offence |
| `DIVISION` | Police division |
| `NEIGHBOURHOOD_158` | Neighbourhood name |
| `PREMISES_TYPE` | Type of premises |
| `LONG_WGS84`, `LAT_WGS84` | Geographic coordinates |

**Data cleaning notes:**
- Records with `NEIGHBOURHOOD_158 == "NSA"` are treated as unknown and excluded from neighbourhood analysis
- Records with zero coordinates `(0.0, 0.0)` are excluded from geographic analysis

---

## Features

- Modular, reusable analytics functions in `src/`
- Clean separation between data logic and UI layer
- Interactive multi-page Streamlit dashboard
- Automated test suite with TDD evidence
- Intentional refactoring tasks documented in the technical report
