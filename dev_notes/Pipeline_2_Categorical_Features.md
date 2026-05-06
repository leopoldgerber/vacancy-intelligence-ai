# Pipeline 2 - Categorical Features

## Overview

This note documents the implementation of the Categorical Features layer in Pipeline 2.

The purpose of this feature layer is to persist stable categorical vacancy attributes that are required for downstream ML workflows, especially models that can work with categorical inputs such as CatBoost.

Categorical Features are stored as a separate feature engineering output instead of being encoded immediately. Encoding and model-specific preprocessing are intentionally left for the ML pipeline.

## Purpose

The Categorical Features layer preserves core business categories from vacancy snapshots in a normalized, reusable form.

The feature layer supports:

- future ML feature dataset assembly;
- model training with categorical columns;
- debugging and feature inspection;
- downstream segmentation;
- future AI context and recommendation logic.

## Source Data

The feature layer uses data from `vacancy_snapshots`.

The relevant source fields are:

- `city`
- `region`
- `profile`
- `employment_type`
- `work_experience`
- `work_schedule`

The shared feature snapshot loader was extended to include all required categorical fields.

## Table

A new table was added:

```text
categorical_features
```

The table stores one feature row per vacancy snapshot and feature run.

## Model

A new SQLAlchemy model was added:

```text
CategoricalFeature
```

Model file:

```text
app/db/models/categorical_feature.py
```

The model is registered in:

```text
app/db/models_registry.py
```

## Granularity

One row in `categorical_features` represents:

```text
feature_run_id + client_id + company_id + vacancy_id + date_day
```

This keeps the feature layer aligned with the other Pipeline 2 feature tables.

## Stored Fields

The table stores:

- `id`
- `feature_run_id`
- `client_id`
- `company_id`
- `vacancy_id`
- `date_day`
- `city`
- `region`
- `profile`
- `employment_type`
- `work_experience`
- `work_schedule`
- `created_at`

## Constraints

A unique constraint was added to prevent duplicate feature rows within the same feature run:

```text
feature_run_id + client_id + company_id + vacancy_id + date_day
```

Constraint name:

```text
uq_categorical_features_feature_run_snapshot
```

## Normalization Logic

Categorical values are normalized before saving.

The normalization rules are:

- `None` becomes `unknown`
- empty strings become `unknown`
- whitespace-only strings become `unknown`
- regular values are stripped from leading and trailing spaces
- original casing is preserved

Lowercasing is intentionally not applied, because these values should remain readable for debugging, reporting, and later inspection.

## Builder

A new builder module was added:

```text
app/services/features/categorical_feature_builders.py
```

The builder contains:

- `normalize_category_value`
- `build_categorical_feature_dataframe`
- `build_categorical_feature_rows`

The builder transforms the snapshot dataframe into persistence-ready categorical feature rows.

## Persistence

The feature persistence layer was extended with:

```text
save_categorical_features
```

File:

```text
app/services/features/persistence.py
```

This function saves rows into `categorical_features` and returns the created model objects.

## Pipeline Runner

A new runner was added:

```text
app/services/features/run_categorical_features_pipeline.py
```

The runner performs the following steps:

1. Build a feature run name.
2. Build a feature report name.
3. Load snapshot data for `client_id + date_from + date_to`.
4. Save a `feature_runs` record.
5. Build categorical feature rows.
6. Save rows into `categorical_features`.
7. Update `feature_count`.
8. Return a technical run response.

For empty input data, the runner saves a `feature_runs` row with:

```text
status = no_data
is_success = false
snapshot_count = 0
feature_count = 0
```

No rows are written to `categorical_features` in the no-data scenario.

## Service Layer

The feature service layer was extended with:

```text
run_categorical_features
```

File:

```text
app/services/features/service.py
```

This function opens a database session and delegates execution to the categorical feature pipeline runner.

## API Endpoint

A new endpoint was added:

```text
POST /pipeline-2/features/categorical/run
```

The endpoint accepts form fields:

- `client_id`
- `date_from`
- `date_to`

The endpoint returns the standard feature run response:

- `feature_run_id`
- `feature_run_name`
- `status`
- `is_success`
- `snapshot_count`
- `feature_count`
- `report_name`

## Makefile Command

A Makefile command was added:

```text
make pipeline-2-categorical-features
```

The local data setup command was also extended to run categorical features after the previous Pipeline 2 feature layers.

## Tests

Unit tests were added for the categorical feature builder:

```text
tests/unit/test_categorical_feature_builders.py
```

The tests cover:

- regular category normalization;
- `None` handling;
- empty string handling;
- whitespace-only handling;
- dataframe building;
- feature row building;
- empty dataframe behavior.

API tests were added:

```text
tests/api/test_pipeline_2_categorical_features_success.py
tests/api/test_pipeline_2_categorical_features_errors.py
```

The API tests cover:

- successful endpoint execution;
- creation of a `feature_runs` row;
- creation of `categorical_features` rows;
- correct `feature_count`;
- correct category normalization;
- no-data behavior.

The shared test cleanup configuration was updated to include `CategoricalFeature`.

## Current Status

The Categorical Features layer is implemented, integrated into the API, connected to the local Makefile workflow, and covered by unit and API tests.

This feature layer is ready to be used later in the final Pipeline 2 feature dataset assembly and in Pipeline 3 ML workflows.
