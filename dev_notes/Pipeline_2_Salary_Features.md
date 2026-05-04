# Pipeline 2: Salary Feature Engineering

## Overview

Pipeline 2 Salary Feature Engineering is the first feature-oriented layer built
after the Analytics Summary layer.

Its purpose is to transform vacancy snapshot salary information into reusable
machine-learning-friendly features. The salary feature layer is not a report-only
analytics module. It is designed as a feature engineering component that can later
be reused by:

1. ML prediction pipelines.
2. AI context generation.
3. Recommendation logic.
4. Additional analytical validation if needed.

The first implemented salary feature version focuses on row-level salary signals
and leave-one-company-out salary benchmarks across competitive segments.

---

## Feature Engineering Goal

The goal of this layer is to answer one core question for every vacancy snapshot:

```text
How does this company's salary level compare with the salary level of other
companies in the same competitive context?
```

The feature layer is built at snapshot level.

One feature row corresponds to:

```text
client_id + company_id + vacancy_id + date_day
```

This keeps the feature output aligned with `vacancy_snapshots` and prepares the
project for future ML training where `callbacks` will be used as the target.

---

## High-Level Flow

```text
vacancy_snapshots
    ↓
load feature snapshot data
    ↓
calculate salary_mid
    ↓
calculate company salary medians
    ↓
calculate leave-one-company-out market medians
    ↓
calculate salary ratio features
    ↓
feature_runs
    ↓
salary_features
```

---

## Main Components

### Feature Run Layer

A separate run table was added for feature engineering.

This keeps feature engineering independent from analytics summary runs.

Implemented table and model:

```text
feature_runs
FeatureRun
```

Purpose:

- track feature engineering executions;
- store client and period metadata;
- track execution status;
- store input snapshot count;
- store generated feature row count;
- link execution with future feature reports.

Main fields:

```text
id
feature_run_name
client_id
date_from
date_to
status
is_success
snapshot_count
feature_count
report_name
created_at
```

Supported statuses:

```text
success
failed
no_data
```

---

### Salary Feature Table

Implemented table and model:

```text
salary_features
SalaryFeature
```

Purpose:

- store salary-related features for each vacancy snapshot;
- keep feature values tied to a specific feature run;
- support later ML dataset construction;
- support reusable salary context for later AI and recommendation layers.

Granularity:

```text
feature_run_id + client_id + company_id + vacancy_id + date_day
```

Duplicate protection is enforced through a unique constraint on:

```text
feature_run_id
client_id
company_id
vacancy_id
date_day
```

---

## Salary Feature Logic

### Salary Midpoint

The main salary value is `salary_mid`.

Raw `salary_from` and `salary_to` are used only to calculate `salary_mid`; they
are not stored as separate salary features in the first MVP version.

Calculation logic:

```text
if salary_from exists and salary_to exists:
    salary_mid = (salary_from + salary_to) / 2

elif salary_from exists:
    salary_mid = salary_from

elif salary_to exists:
    salary_mid = salary_to

else:
    salary_mid = 0
```

The value `0` is intentionally used when salary is missing. This makes missing
salary a strong model signal while keeping the feature output numeric and
machine-learning-friendly.

An additional boolean feature is stored:

```text
salary_is_specified
```

It is calculated as:

```text
1 if salary_from or salary_to exists else 0
```

---

## Leave-One-Company-Out Salary Benchmark

The salary benchmark is calculated for each company against the other companies
in the same `client_id` context.

For example, if the competitive context contains three companies:

```text
Company A
Company B
Company C
```

Then the market median is calculated as:

```text
for Company A: median salary of Company B + Company C
for Company B: median salary of Company A + Company C
for Company C: median salary of Company A + Company B
```

This prevents a company from influencing its own benchmark.

The main benchmark metric is a ratio:

```text
salary_ratio_to_market = company_salary_median / market_salary_median_excl_company
```

If the market median excluding the company is `0`, the ratio is saved as `0`.

---

## Segment Levels

Salary benchmarks are calculated across three segment levels:

```text
city
profile
city + profile
```

This allows the same salary logic to be reused for different competitive
contexts.

Implemented feature columns:

```text
company_salary_median_by_city
market_salary_median_excl_company_by_city
salary_ratio_to_market_by_city

company_salary_median_by_profile
market_salary_median_excl_company_by_profile
salary_ratio_to_market_by_profile

company_salary_median_by_city_profile
market_salary_median_excl_company_by_city_profile
salary_ratio_to_market_by_city_profile
```

---

## API Layer

Implemented endpoint:

```text
POST /pipeline-2/features/salary/run
```

Input fields:

```text
client_id
date_from
date_to
```

The endpoint intentionally does not accept `city` or `profile` filters.

Reason:

Feature engineering should build a complete feature dataset for the selected
client and period. Segment logic is calculated inside the feature layer rather
than by filtering the input dataset.

Response structure:

```json
{
  "feature_run_id": 1,
  "feature_run_name": "features_YYYY-MM-DD_HH-MM-SS",
  "status": "success",
  "is_success": true,
  "snapshot_count": 17145,
  "feature_count": 17145,
  "report_name": "features_YYYY-MM-DD_HH-MM-SS.md"
}
```

---

## Main Modules

```text
app/services/features/constants.py
app/services/features/name_builders.py
app/services/features/data_loaders.py
app/services/features/persistence.py
app/services/features/salary_feature_builders.py
app/services/features/run_salary_features_pipeline.py
app/services/features/service.py
```

API modules:

```text
app/api/schemas/features.py
app/api/routes/features.py
```

Database models:

```text
app/db/models/feature_run.py
app/db/models/salary_feature.py
```

---

## Makefile Command

Added command:

```makefile
pipeline-2-salary-features:
	curl -X POST http://127.0.0.1:8000/pipeline-2/features/salary/run \
		-F "client_id=1" \
		-F "date_from=2025-08-01" \
		-F "date_to=2025-08-21"
```

Usage:

```bash
make pipeline-2-salary-features
```

---

## Tests

Salary Feature Engineering is covered by unit and API tests.

### Unit Tests

```text
tests/unit/test_salary_feature_builders.py
```

Covered logic:

- salary midpoint calculation with both salary bounds;
- salary midpoint calculation with only `salary_from`;
- salary midpoint calculation with only `salary_to`;
- salary midpoint calculation when salary is missing;
- salary ratio calculation;
- zero-market-median handling;
- salary feature dataframe creation;
- salary feature row creation;
- empty input behavior.

### API Tests

```text
tests/api/test_pipeline_2_salary_features_success.py
tests/api/test_pipeline_2_salary_features_errors.py
```

Covered scenarios:

- successful salary feature pipeline execution;
- creation of `feature_runs`;
- creation of `salary_features`;
- correct `snapshot_count`;
- correct `feature_count`;
- no-data scenario;
- no feature rows created when input data is empty.

`tests/conftest.py` was updated to clear:

```text
salary_features
feature_runs
```

before dependent parent tables.

---

## Current Status

Pipeline 2 Salary Feature Engineering is implemented and tested at MVP level.

Completed:

- `feature_runs` table and model;
- `salary_features` table and model;
- salary midpoint calculation;
- salary availability flag;
- leave-one-company-out salary benchmark by city;
- leave-one-company-out salary benchmark by profile;
- leave-one-company-out salary benchmark by city + profile;
- salary ratio features;
- feature pipeline runner;
- API endpoint;
- Makefile command;
- unit tests;
- API success test;
- API no-data test.

This layer is now ready to be reused by later Pipeline 2 feature directions and,
eventually, by Pipeline 3 ML training.

---

## Future Improvements

Possible future improvements:

- add feature reports for feature engineering runs;
- add expected error handling for missing `client_id`;
- add logging for feature pipeline execution;
- add additional salary features after model experimentation;
- add historical salary movement features;
- add time-aware benchmark calculations to avoid leakage in future ML training;
- add integration tests with a dedicated test database;
- connect salary features to a broader final ML feature dataset.
