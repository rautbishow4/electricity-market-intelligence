
# European Electricity Market Intelligence

## Overview

A data engineering and analytics portfolio project using Germany's electricity market data from SMARD.

The goal is to build a repeatable pipeline that collects electricity market prices, load, and renewable generation data and prepares it for SQL-based analysis and visualization.

## Current progress

- Retrieved day-ahead electricity prices at 15-minute resolution
- Retrieved electricity load and renewable generation at hourly resolution
- Built a Python ingestion script using the SMARD API
- Saved raw datasets locally as CSV files
- Implemented data-quality checks for missing values, duplicates, and time intervals
- Investigated missing values returned by the source API

## Technology stack

- Python
- Requests
- Pandas
- Git and GitHub

## Data source

SMARD — Germany's electricity market data platform:
https://www.smard.de/

Community API documentation:
https://github.com/bundesAPI/smard-api

## Run locally

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the ingestion pipeline:

```bash
python ingest_smard.py
```

Run data validation:

```bash
python validate_smard_data.py
```

The pipeline writes downloaded CSV files to `data/raw/`. These generated files are excluded from Git.

## Planned improvements

- Improve incremental ingestion and historical backfills
- Add data-quality and API error handling
- Transform data into a consistent analytical model
- Load data into PostgreSQL
- Build SQL-based KPIs and a data warehouse
- Create an interactive Power BI dashboard
- Explore electricity price forecasting
