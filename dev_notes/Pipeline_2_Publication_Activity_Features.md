# Pipeline 2: Publication Activity Features

## Overview

Publication Activity Features are the second implemented feature engineering
layer in Pipeline 2.

This layer transforms daily publication and promotion signals from vacancy
snapshots into reusable machine-learning-oriented features.

The layer is intentionally named **Publication Activity Features** instead of
**Tariff Features**, because the source fields do not only describe a static
vacancy tariff. They describe whether a vacancy had publication, boost or
promotion activity on a specific snapshot day.

The implemented feature layer is designed for reuse in:

1. future ML training datasets;
2. future forecasting logic;
3. future recommendation scenarios;
4. future AI context generation.

---

## Feature Goal

The goal of this feature layer is to capture how recently and how strongly a
vacancy was actively published or promoted.

The layer answers two main questions for each vacancy snapshot:

- Was there publication or promotion activity on this day?
- How many days have passed since the last known publication activity?

This is important because vacancies may remain active and visible in search even
when they are not republished or boosted on a specific day.

---

## Business Logic

The source fields are:

```text
standard
standard_plus
premium
```

These fields are interpreted as daily publication activity flags.

Meaning:

- `standard = 1` means Standard publication activity happened on that day;
- `standard_plus = 1` means Standard Plus publication activity happened on that day;
- `premium = 1` means Premium publication activity happened on that day;
- all three fields equal to `0` means the vacancy is still active, but there was
  no new publication or promotion activity on that snapshot day.

This means that `0` is not treated as an unknown tariff. It is treated as a real
state: active vacancy without publication activity on that day.

---

## Implemented Features

### `publication_activity_level`

Represents the strength of publication activity on the snapshot day.

Calculation priority:

```text
premium = 1        -> 3
standard_plus = 1 -> 2
standard = 1      -> 1
all zero          -> 0
```

The priority order is:

```text
premium > standard_plus > standard > no_activity
```

Interpretation:

```text
0 = no publication activity
1 = Standard publication activity
2 = Standard Plus publication activity
3 = Premium publication activity
```

---

### `days_since_last_publication_activity`

Represents how many days have passed since the previous publication activity for
the same vacancy.

The feature is calculated inside each vacancy history group:

```text
client_id + company_id + vacancy_id
```

Rows are ordered by:

```text
date_day
```

Rules:

```text
0  = publication activity happened on the current day
1  = previous activity happened one day before
2  = previous activity happened two days before
-1 = no prior publication activity is known before this day
```

Example:

```text
date_day     publication_activity_level   days_since_last_publication_activity
2025-08-01   1                            0
2025-08-02   0                            1
2025-08-03   0                            2
2025-08-04   2                            0
2025-08-05   0                            1
```

---

## Forecasting and Recommendation Note

For historical feature engineering, `publication_activity_level` is calculated
from actual snapshot data.

For future forecasting and recommendation logic, this feature can later be used
as a controllable planned action.

For example, a future recommendation engine may evaluate scenarios such as:

```text
0 = do not republish or boost
1 = use Standard publication
2 = use Standard Plus publication
3 = use Premium publication
```

In that future setup, `days_since_last_publication_activity` would need to be
recalculated based on the planned action.

This action/scenario inference functionality is intentionally not implemented in
this step. The current implementation only builds historical publication
activity features from existing vacancy snapshots.

---

## High-Level Flow

```text
vacancy_snapshots
    ↓
feature snapshot loader
    ↓
publication activity feature builder
    ↓
feature_runs
    ↓
publication_activity_features
    ↓
API response
```

---

## Database Tables

### `feature_runs`

Stores one feature engineering execution record.

Purpose:

- track feature engineering runs;
- store client and date period;
- store execution status;
- store input snapshot count;
- store output feature row count;
- link a run with a report name.

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

---

### `publication_activity_features`

Stores publication activity features for vacancy snapshots.

One row corresponds to one vacancy snapshot inside one feature run.

Granularity:

```text
feature_run_id + client_id + company_id + vacancy_id + date_day
```

Main fields:

```text
id
feature_run_id
client_id
company_id
vacancy_id
date_day
publication_activity_level
days_since_last_publication_activity
created_at
```

Duplicate protection is handled by the unique constraint:

```text
feature_run_id
client_id
company_id
vacancy_id
date_day
```

---

## Main Components

### Data Loader

The feature data loader was extended to include publication activity source
fields.

Main module:

```text
app/services/features/data_loaders.py
```

Loaded fields include:

```text
client_id
company_id
vacancy_id
date_day
salary_from
salary_to
city
profile
standard
standard_plus
premium
```

The loader intentionally does not apply `city` or `profile` filters. Feature
engineering uses the full snapshot set for the selected `client_id` and period.

---

### Feature Builder

Main module:

```text
app/services/features/publication_activity_feature_builders.py
```

Implemented functions include:

```text
calculate_publication_activity_level
add_publication_activity_level
add_days_since_last_publication_activity
build_publication_activity_feature_dataframe
build_publication_activity_feature_rows
```

The builder contains the main feature calculation logic and does not access the
database directly.

---

### Persistence Layer

Main module:

```text
app/services/features/persistence.py
```

Implemented persistence function:

```text
save_publication_activity_features
```

The function stores generated publication activity feature rows in
`publication_activity_features`.

---

### Pipeline Runner

Main module:

```text
app/services/features/run_publication_activity_features_pipeline.py
```

The runner performs the full publication activity feature flow:

1. Build feature run name.
2. Load vacancy snapshots.
3. Save `feature_runs` record.
4. Build publication activity feature rows.
5. Save `publication_activity_features` rows.
6. Update `feature_count`.
7. Return feature run response.

---

### Service Layer

Main module:

```text
app/services/features/service.py
```

Implemented service function:

```text
run_publication_activity_features
```

The service opens the database session and calls the publication activity feature
pipeline runner.

---

## API Endpoint

Implemented endpoint:

```text
POST /pipeline-2/features/publication-activity/run
```

Input form fields:

```text
client_id
date_from
date_to
```

Successful response structure:

```json
{
  "feature_run_id": 1,
  "feature_run_name": "features_2026-05-04_21-55-50",
  "status": "success",
  "is_success": true,
  "snapshot_count": 5,
  "feature_count": 5,
  "report_name": "features_2026-05-04_21-55-50.md"
}
```

No-data response structure:

```json
{
  "feature_run_id": 1,
  "feature_run_name": "features_2026-05-04_21-55-50",
  "status": "no_data",
  "is_success": false,
  "snapshot_count": 0,
  "feature_count": 0,
  "report_name": "features_2026-05-04_21-55-50.md"
}
```

---

## Makefile Command

Implemented command:

```makefile
pipeline-2-publication-activity-features:
	curl -X POST http://127.0.0.1:8000/pipeline-2/features/publication-activity/run \
		-F "client_id=1" \
		-F "date_from=2025-08-01" \
		-F "date_to=2025-08-21"
```

Run command:

```bash
make pipeline-2-publication-activity-features
```

---

## Tests

Publication Activity Features are covered by unit tests and API tests.

### Unit Tests

```text
tests/unit/test_publication_activity_feature_builders.py
```

Covered scenarios include:

- Premium activity level calculation;
- Standard Plus activity level calculation;
- Standard activity level calculation;
- no-activity level calculation;
- days since last publication activity;
- no prior activity case;
- empty dataframe behavior;
- feature row generation.

### API Tests

```text
tests/api/test_pipeline_2_publication_activity_features_success.py
tests/api/test_pipeline_2_publication_activity_features_errors.py
```

Covered scenarios include:

- successful publication activity feature run;
- creation of `feature_runs` record;
- creation of `publication_activity_features` rows;
- correct `feature_count`;
- correct `publication_activity_level` values;
- correct `days_since_last_publication_activity` values;
- no-data behavior.

---

## Current Status

Publication Activity Features are implemented as a production-like feature
engineering layer inside Pipeline 2.

Completed:

- database model;
- Alembic migration;
- feature loader update;
- feature builder;
- persistence function;
- pipeline runner;
- service wrapper;
- API endpoint;
- Makefile command;
- unit tests;
- API tests.

This layer is ready to be reused later by the ML pipeline and future
recommendation logic.

---

## Future Improvements

Possible future improvements:

- add planned-action feature generation for forecasting scenarios;
- add recommendation scenario simulation for `publication_activity_level`;
- add rolling activity counts for the last 3, 7 and 14 days;
- add separate premium activity recency features;
- add activity pattern features for Standard Plus cycles;
- add consolidated feature dataset assembly after all feature directions are
  implemented;
- move tests to a dedicated test database to avoid modifying local development
  data.
