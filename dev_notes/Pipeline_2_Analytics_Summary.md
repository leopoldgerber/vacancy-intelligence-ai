# Pipeline 2: Analytics Summary

## Overview

Pipeline 2 starts the analytical layer of the project.

The first implemented part is **Analytics Summary**. It calculates aggregated
summary metrics from already ingested vacancy snapshots and stores the results
in PostgreSQL.

This layer does not read uploaded `.xlsx` files directly. It works only with
data that has already passed Pipeline 1 and has been saved to the database.

The first Analytics Summary flow is responsible for:

1. Reading vacancy snapshot data from PostgreSQL.
2. Applying optional `city` and `profile` filters.
3. Creating an analytics run record.
4. Calculating market summary metrics.
5. Calculating target client summary metrics.
6. Calculating competitor summary metrics.
7. Saving calculated summaries in PostgreSQL.
8. Generating a shared `.md` analytics summary report.
9. Handling no-data scenarios safely.

---

## Pipeline Goal

The goal of Pipeline 2 Analytics Summary is to create the first structured
analytical view over the ingested vacancy data.

The summary layer answers three main questions:

- What does the competitive context look like for the selected client?
- How does the target client perform within that context?
- What do competitors look like in the same client-scoped dataset?

This stage is focused only on analytics. Feature engineering and AI context
preparation are intentionally kept separate and will be implemented later.

---

## Scope

The implemented Analytics Summary layer includes:

```text
market_summary
client_summary
competitor_summary
```

The layer does not yet include:

```text
slot_analytics
tariff_analytics
text_quality_analytics
salary_analytics
feature_engineering
AI insight context
```

These parts are planned as separate analytical or downstream stages.

---

## High-Level Flow

```text
POST /pipeline-2/analytics/summary/run
    ↓
read request fields
    ↓
load vacancy_snapshots from PostgreSQL
    ↓
apply optional city/profile filters
    ↓
create analytics_runs record
    ↓
calculate market_summary
    ↓
calculate client_summary
    ↓
calculate competitor_summary
    ↓
save summaries to PostgreSQL
    ↓
generate .md report
    ↓
return API response
```

---

## API Endpoint

Implemented endpoint:

```text
POST /pipeline-2/analytics/summary/run
```

Main route module:

```text
app/api/routes/analytics.py
```

Response schema:

```text
app/api/schemas/analytics.py
```

---

## Request Fields

The endpoint accepts form fields:

```text
client_id
date_from
date_to
city
profile
```

### Required Fields

```text
client_id
date_from
date_to
```

### Optional Fields

```text
city
profile
```

Optional filter logic:

- empty `city` means all cities;
- empty `profile` means all profiles;
- filled `city` limits the analysis to the selected city;
- filled `profile` limits the analysis to the selected profile;
- filled `city` and `profile` limit the analysis to that segment.

Example default values used in local development:

```text
client_id = 1
date_from = 2025-08-01
date_to = 2025-08-21
city = empty
profile = empty
```

---

## Data Sources

Pipeline 2 Analytics Summary reads from tables created and populated by
Pipeline 1.

Main source tables:

```text
clients
companies
vacancies
vacancy_snapshots
```

The main analytical source is:

```text
vacancy_snapshots
```

The table stores historical vacancy observations and is used for all summary
calculations.

---

## Client and Competitor Logic

The project does not store the entire labor market. It stores the target client
and relevant competitors for that target client.

The `clients` table contains the target client reference.

Important rule:

```text
clients.name = target client's company_name
```

The `companies` table contains both the target client company and competitor
companies within the selected client context.

Target client logic:

```text
companies.name = clients.name
```

Competitor logic:

```text
companies.name != clients.name
```

This means:

- `market_summary` uses target client + competitors;
- `client_summary` uses only the target client;
- `competitor_summary` uses only competitors.

---

## Main Components

### Analytics Run Layer

The analytics run layer stores technical metadata about each Analytics Summary
execution.

Main modules:

```text
app/db/models/analytics_run.py
app/services/analytics/name_builders.py
app/services/analytics/repositories.py
app/services/analytics/persistence.py
app/services/analytics/run_analytics_pipeline.py
app/services/analytics/service.py
```

Analytics run records are saved to:

```text
analytics_runs
```

---

### Data Loading Layer

The data loading layer reads snapshot data from PostgreSQL and returns pandas
DataFrames for calculation functions.

Main module:

```text
app/services/analytics/data_loaders.py
```

Implemented loaders:

```text
load_snapshot_data
load_client_snapshot_data
load_competitor_snapshot_data
```

Loader roles:

- `load_snapshot_data` loads target client + competitors;
- `load_client_snapshot_data` loads only the target client;
- `load_competitor_snapshot_data` loads only competitors.

---

### Market Summary Layer

The market summary layer calculates aggregated metrics for the full
client-scoped competitive context.

Main module:

```text
app/services/analytics/market_summary_builders.py
```

Results are saved to:

```text
market_summaries
```

The table represents the analytical context made of:

```text
target client + relevant competitors
```

It does not represent the full labor market.

---

### Client Summary Layer

The client summary layer calculates metrics only for the target client.

Main module:

```text
app/services/analytics/client_summary_builders.py
```

Results are saved to:

```text
client_summaries
```

Target client records are identified by:

```text
companies.name = clients.name
```

---

### Competitor Summary Layer

The competitor summary layer calculates metrics only for competitors in the
same client-scoped dataset.

Main module:

```text
app/services/analytics/competitor_summary_builders.py
```

Results are saved to:

```text
competitor_summaries
```

Competitor records are identified by:

```text
companies.name != clients.name
```

---

### Report Layer

Analytics Summary generates one shared `.md` report for the run.

Main modules:

```text
app/services/analytics/report_builders.py
app/services/analytics/report_writers.py
```

Reports are saved to:

```text
artifacts/reports/pipeline_2/analytics
```

The report includes:

- run information;
- selected `city` and `profile` filters;
- market summary;
- client summary;
- competitor summary.

---

## Database Tables

### `analytics_runs`

Stores one Pipeline 2 analytics execution record.

Purpose:

- track analytics execution status;
- store the selected client and period;
- store the number of input snapshot rows;
- link the run with generated reports and summary tables.

Main fields:

```text
id
analytics_name
client_id
date_from
date_to
status
is_success
snapshot_count
report_name
created_at
```

---

### `market_summaries`

Stores the aggregated summary for the full client-scoped competitive context.

Purpose:

- summarize target client + competitor data;
- provide high-level analytical metrics;
- support reporting and later analytical layers.

Main metrics include:

```text
total_snapshot_count
total_company_count
total_vacancy_count
total_callbacks
avg_callbacks
median_callbacks
mode_city
mode_region
mode_profile
mode_tariff
mode_work_schedule
mode_work_experience
mode_employment_type
median_salary_from
median_salary_to
salary_specified_share
salary_missing_share
```

---

### `client_summaries`

Stores the aggregated summary for the target client only.

Purpose:

- calculate target client-specific metrics;
- prepare comparison against market and competitors;
- support future recommendations and AI context.

Target client detection rule:

```text
companies.name = clients.name
```

---

### `competitor_summaries`

Stores the aggregated summary for competitors only.

Purpose:

- calculate competitor-specific metrics;
- separate competitor activity from target client activity;
- prepare future competitor analytics and comparison layers.

Competitor detection rule:

```text
companies.name != clients.name
```

---

## Reports

Analytics Summary generates one `.md` report per run.

Report content is based on calculated and saved summary results.

Report path:

```text
artifacts/reports/pipeline_2/analytics
```

Report names use the analytics run timestamp format:

```text
analytics_YYYY-MM-DD_HH-MM-SS.md
```

The report currently contains:

```text
Run information
Market summary
Client summary
Competitor summary
```

---

## No-Data Handling

If no `vacancy_snapshots` are found for the selected client, period and filters,
the pipeline creates an `analytics_runs` record with:

```text
status = no_data
is_success = false
snapshot_count = 0
```

In this case, summary tables are not populated.

A technical `.md` report is still generated.

---

## Makefile Command

Pipeline 2 Summary can be triggered through Makefile.

```makefile
pipeline-2-summary:
	curl -X POST http://127.0.0.1:8000/pipeline-2/analytics/summary/run \
		-F "client_id=1" \
		-F "date_from=2025-08-01" \
		-F "date_to=2025-08-21" \
		-F "city=" \
		-F "profile="
```

Run command:

```bash
make pipeline-2-summary
```

---

## Tests

Analytics Summary is covered by unit tests and API tests.

### Unit Tests

```text
tests/unit/test_market_summary_builders.py
tests/unit/test_client_summary_builders.py
tests/unit/test_competitor_summary_builders.py
```

Covered areas include:

- snapshot counts;
- company counts;
- vacancy counts;
- total callbacks;
- average callbacks;
- median callbacks;
- most frequent categorical values;
- salary specified and missing shares;
- empty DataFrame behavior.

### API Tests

```text
tests/api/test_pipeline_2_summary_success.py
tests/api/test_pipeline_2_summary_errors.py
```

Covered scenarios include:

- successful Pipeline 2 Summary execution;
- saving `analytics_runs`;
- saving `market_summaries`;
- saving `client_summaries`;
- saving `competitor_summaries`;
- `no_data` execution path.

---

## Current Status

Pipeline 2 Analytics Summary is complete at the first analytical layer level.

Completed:

- summary analytics endpoint;
- analytics run persistence;
- market summary calculation and persistence;
- client summary calculation and persistence;
- competitor summary calculation and persistence;
- shared `.md` report generation;
- optional `city` and `profile` filters;
- no-data handling;
- unit tests;
- API tests;
- Makefile command.

The next planned analytical layers are:

```text
salary analytics
slot analytics
tariff analytics
text quality analytics
```

Feature engineering and AI context preparation remain separate downstream parts
of Pipeline 2 and will be implemented later.
