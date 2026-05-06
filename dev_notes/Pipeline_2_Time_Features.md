# Pipeline 2: Time Features

## Overview

The Time Features layer is part of Pipeline 2 Feature Engineering.

It converts temporal fields from vacancy snapshots into structured, reusable
features that can later be used by machine learning models, analytics checks and
AI context generation.

This layer does not generate a separate business analytics report. Its purpose is
to create production-like feature outputs that can be joined into the future ML
training dataset.

---

## Feature Layer Goal

The goal of Time Features is to describe the temporal context of each vacancy
snapshot.

The layer answers questions such as:

- At what hour was the vacancy originally published?
- On which weekday was the vacancy originally published?
- In which calendar month and week was it published?
- Was the publication date on a weekend?
- How old was the vacancy on the snapshot date?

These features are useful because candidate response behavior may depend on
publication timing and vacancy age.

---

## Input Data

The layer uses vacancy snapshot data loaded from:

```text
vacancy_snapshots
```

Required input fields:

```text
client_id
company_id
vacancy_id
date_day
publication_date
```

The shared feature loader was extended to include:

```text
publication_date
```

Main loader module:

```text
app/services/features/data_loaders.py
```

---

## Output Table

Time features are stored in:

```text
time_features
```

The table stores one feature row per vacancy snapshot and feature run.

Granularity:

```text
feature_run_id + client_id + company_id + vacancy_id + date_day
```

This makes the table compatible with the other Pipeline 2 feature layers.

---

## Database Model

Implemented SQLAlchemy model:

```text
app/db/models/time_feature.py
```

Database table:

```text
time_features
```

Main fields:

```text
id
feature_run_id
client_id
company_id
vacancy_id
date_day
publication_hour
publication_day_of_week
publication_month
publication_week
is_weekend
vacancy_age_days
created_at
```

A unique constraint prevents duplicate feature rows inside the same feature run:

```text
feature_run_id
client_id
company_id
vacancy_id
date_day
```

The model was added to:

```text
app/db/models_registry.py
```

An Alembic migration was created and applied for the `time_features` table.

---

## Feature Definitions

### `publication_hour`

Publication hour extracted from `publication_date`.

Logic:

```text
publication_date.hour
```

Fallback:

```text
-1 if publication_date is missing
```

---

### `publication_day_of_week`

Weekday extracted from `publication_date`.

Python weekday convention is used:

```text
0 = Monday
6 = Sunday
```

Fallback:

```text
-1 if publication_date is missing
```

---

### `publication_month`

Calendar month extracted from `publication_date`.

Fallback:

```text
-1 if publication_date is missing
```

---

### `publication_week`

ISO calendar week extracted from `publication_date`.

Fallback:

```text
-1 if publication_date is missing
```

---

### `is_weekend`

Boolean flag showing whether the original publication date was on Saturday or
Sunday.

Logic:

```text
True if publication_date.weekday() in [5, 6]
False otherwise
```

Fallback:

```text
False if publication_date is missing
```

---

### `vacancy_age_days`

Number of days between the snapshot date and the original publication date.

Logic:

```text
date_day - publication_date
```

The result is measured in days.

Fallbacks:

```text
-1 if date_day or publication_date is missing
0 if the calculated age is negative
```

Negative values are clipped to `0` to protect the feature dataset from invalid
source-date combinations.

---

## Main Components

### Builder Layer

Implemented module:

```text
app/services/features/time_feature_builders.py
```

Main functions:

```text
calculate_publication_hour
calculate_publication_day_of_week
calculate_publication_month
calculate_publication_week
calculate_is_weekend
calculate_vacancy_age_days
build_time_feature_dataframe
build_time_feature_rows
```

The builder layer is database-independent and works with pandas DataFrames.

---

### Persistence Layer

The shared feature persistence layer was extended with:

```text
save_time_features
```

Implemented in:

```text
app/services/features/persistence.py
```

---

### Pipeline Runner

Implemented runner:

```text
app/services/features/run_time_features_pipeline.py
```

The runner performs the full feature flow:

1. Build a feature run name.
2. Load vacancy snapshots for `client_id + date range`.
3. Save a `feature_runs` record.
4. Build time feature rows.
5. Save rows to `time_features`.
6. Update `feature_count`.
7. Return a structured API response.

If no snapshots are found, the runner creates a `feature_runs` record with:

```text
status = no_data
is_success = false
feature_count = 0
```

---

### Service Layer

The feature service layer was extended with:

```text
run_time_features
```

Implemented in:

```text
app/services/features/service.py
```

---

## API Endpoint

Implemented endpoint:

```text
POST /pipeline-2/features/time/run
```

Request form fields:

```text
client_id
date_from
date_to
```

Response schema:

```text
FeatureRunResponse
```

The endpoint is registered under the shared Pipeline 2 feature router:

```text
app/api/routes/features.py
```

---

## Makefile Command

Added command:

```bash
make pipeline-2-time-features
```

The command calls:

```text
POST /pipeline-2/features/time/run
```

with the default local development values:

```text
client_id = 1
date_from = 2025-08-01
date_to = 2025-08-21
```

The local data setup command was also extended to run Time Features after the
other Pipeline 2 feature layers.

---

## Tests

### Unit Tests

Added unit tests:

```text
tests/unit/test_time_feature_builders.py
```

Covered logic:

- publication hour calculation;
- publication weekday calculation;
- publication month calculation;
- ISO week calculation;
- weekend flag calculation;
- vacancy age calculation;
- negative vacancy age protection;
- missing-date fallback behavior;
- DataFrame builder;
- persistence row builder;
- empty input behavior.

---

### API Tests

Added API tests:

```text
tests/api/test_pipeline_2_time_features_success.py
tests/api/test_pipeline_2_time_features_errors.py
```

Covered scenarios:

- successful Time Feature run;
- creation of a `feature_runs` record;
- creation of `time_features` rows;
- correct `feature_count`;
- correct calculated time feature values;
- no-data scenario;
- no feature rows created in the no-data scenario.

The shared test cleanup configuration was updated to include:

```text
TimeFeature
```

so that test runs remain isolated and repeatable.

---

## Current Status

The Time Features layer is implemented and covered by unit/API tests.

Completed:

- SQLAlchemy model;
- database migration;
- shared loader extension;
- feature builder logic;
- persistence function;
- pipeline runner;
- service wrapper;
- API endpoint;
- Makefile command;
- unit tests;
- API success test;
- API no-data test.

This layer is ready to be used later in the final feature dataset assembly for
Pipeline 3 ML training.

---

## Future Improvements

Possible future improvements:

- add publication time slot buckets;
- add cyclic encoding for weekday, month and hour;
- add separate snapshot-date features in addition to publication-date features;
- add holiday or seasonal indicators;
- add rolling time-based features when historical feature logic is introduced;
- move test execution to a dedicated test database to avoid modifying local dev data.
