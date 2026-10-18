# European Electricity Market Intelligence

## Overview

A data engineering and analytics portfolio project using Germany's electricity market data from SMARD.

The goal is to build a repeatable pipeline that collects electricity market prices, load, and renewable generation data and prepares it for SQL-based analysis and visualization.

## Current progress

- Retrieved day-ahead electricity prices at 15-minute resolution
- Retrieved electricity load and renewable generation data at hourly resolution
- Built a Python ingestion script using the SMARD API
- Saved raw datasets locally as CSV files
- Implemented a data preparation script to clean raw data and create a separate staging layer
- Implemented data-quality checks for missing values, duplicate timestamps, invalid timestamps, and time intervals
- Investigated missing values returned by the source API and refreshed the affected datasets
- Validated the staging datasets, with all five datasets passing the current basic validation checks

## Technology stack

- Python
- Requests
- Pandas
- Git and GitHub

## Data source

SMARD — Germany's electricity market data platform: [https://www.smard.de/](https://www.smard.de/)

Community API documentation: [https://github.com/bundesAPI/smard-api](https://github.com/bundesAPI/smard-api)

## Run locally

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the ingestion pipeline:

```bash
python ingest_smard.py
```

Prepare the staging datasets:

```bash
python prepare_smard_data.py
```

Validate the staging datasets:

```bash
python validate_smard_data.py staging
```

To validate the raw datasets instead:

```bash
python validate_smard_data.py raw
```

The pipeline writes downloaded CSV files to `data/raw/` and prepared datasets to `data/staging/`. These generated files are excluded from Git.

## Planned improvements

- Improve incremental ingestion and historical backfills
- Improve data-quality handling and API error handling
- Transform data into a consistent analytical model
- Load data into PostgreSQL
- Build SQL-based KPIs and a data warehouse
- Create an interactive Power BI dashboard
- Explore electricity price forecasting
