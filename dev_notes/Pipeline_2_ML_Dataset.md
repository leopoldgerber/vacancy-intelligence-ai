# Pipeline 2 - ML Dataset Layer

## Overview

This development note documents the final ML dataset layer added to Pipeline 2.

The purpose of this layer is to materialize a stable, reproducible training dataset from the previously generated feature layers. It acts as the bridge between Pipeline 2 feature engineering and the future Pipeline 3 machine learning stage.

## Motivation

Before this layer, Pipeline 2 generated multiple independent feature tables:

- `salary_features`
- `publication_activity_features`
- `text_features`
- `time_features`
- `categorical_features`

Each table was useful as an isolated feature layer, but ML training needs a single dataset where all features are available in one row per vacancy snapshot.

The project intentionally materializes the final ML dataset instead of rebuilding it dynamically through joins at every training run.

This provides:

- reproducibility of training data;
- easier debugging;
- clear separation between feature generation and model training;
- stable dataset snapshots for future model comparison;
- a production-like artifact between feature engineering and ML training.

## Key Design Decision

The final dataset stores concrete feature values, not only references to feature row IDs.

The project considered storing only links to source feature rows, but this approach was rejected because it would still require repeated joins before every ML training run and would make dataset reproducibility weaker.

Instead, the final dataset is materialized in `ml_feature_rows`.

## New Database Tables

### `ml_dataset_runs`

This table stores metadata for each final ML dataset build.

It records:

- dataset run name;
- client ID;
- date range;
- source feature run IDs;
- run status;
- success flag;
- generated row count;
- report name;
- creation timestamp.

Source feature run references include:

- `salary_feature_run_id`
- `publication_activity_feature_run_id`
- `text_feature_run_id`
- `time_feature_run_id`
- `categorical_feature_run_id`

This makes it possible to identify exactly which feature runs were used to build each materialized ML dataset.

### `ml_feature_rows`

This table stores the final materialized ML dataset.

One row corresponds to one vacancy snapshot:

```text
client_id + company_id + vacancy_id + date_day
```

The table includes:

- technical identifiers;
- target value;
- salary features;
- publication activity features;
- text features;
- time features;
- categorical features.

The target column is:

```text
callbacks
```

## Join Logic

The ML dataset layer joins all feature layers using the same snapshot keys:

```text
client_id
company_id
vacancy_id
date_day
```

The dataset builder uses inner joins. This means a row is included in the final ML dataset only if all required feature layers are available for the same snapshot.

This behavior is intentional because the final ML dataset should contain complete feature rows.

## Source Feature Layers

The final ML dataset currently includes features from the following layers.

### Salary Features

Included fields:

- `salary_mid`
- `salary_is_specified`
- `salary_ratio_to_market_by_city`
- `salary_ratio_to_market_by_profile`
- `salary_ratio_to_market_by_city_profile`

### Publication Activity Features

Included fields:

- `publication_activity_level`
- `days_since_last_publication_activity`

### Text Features

Included fields:

- `title_length`
- `description_length`
- `title_word_count`
- `description_word_count`
- `has_description`
- `description_is_empty`
- `has_salary_mention`
- `has_schedule_mention`
- `has_requirements_mention`
- `has_benefits_mention`
- `has_call_to_action`

### Time Features

Included fields:

- `publication_hour`
- `publication_day_of_week`
- `publication_month`
- `publication_week`
- `is_weekend`
- `vacancy_age_days`

### Categorical Features

Included fields:

- `city`
- `region`
- `profile`
- `employment_type`
- `work_experience`
- `work_schedule`

## Feature Run Selection

The ML dataset pipeline automatically selects the latest successful feature run for each required feature layer.

Feature runs are selected by:

- `client_id`
- `date_from`
- `date_to`
- `status = success`
- feature-specific `feature_run_name` prefix

The feature run name prefixes are:

- `salary_features`
- `publication_activity_features`
- `text_features`
- `time_features`
- `categorical_features`

Feature run names were updated to include these prefixes so that the ML dataset layer can reliably detect the correct latest feature run for each direction.

## New Service Package

A new service package was added:

```text
app/services/ml_dataset/
```

It contains:

- `constants.py`
- `name_builders.py`
- `data_loaders.py`
- `dataset_builders.py`
- `persistence.py`
- `run_ml_dataset_pipeline.py`
- `service.py`

## API Endpoint

A new endpoint was added:

```text
POST /pipeline-2/ml-dataset/run
```

It accepts:

```text
client_id
date_from
date_to
```

It returns:

- `ml_dataset_run_id`
- `dataset_run_name`
- `status`
- `is_success`
- `row_count`
- `report_name`

## Makefile Command

A Makefile command was added for local execution:

```makefile
pipeline-2-ml-dataset:
	curl -X POST http://127.0.0.1:8000/pipeline-2/ml-dataset/run \
		-F "client_id=1" \
		-F "date_from=2025-08-01" \
		-F "date_to=2025-08-21"
```

The local setup command was also extended so that the ML dataset is built after all individual feature layers have been generated.

## Tests Added

Unit test:

```text
tests/unit/test_ml_dataset_builders.py
```

API tests:

```text
tests/api/test_pipeline_2_ml_dataset_success.py
tests/api/test_pipeline_2_ml_dataset_errors.py
```

The tests cover:

- successful dataset build;
- correct feature row materialization;
- correct target value persistence;
- correct source feature run references;
- no-data behavior when required feature runs are missing;
- no ML feature rows created in no-data cases.

## Current Status

The ML Dataset Layer is implemented and covered by unit and API tests.

It completes the first production-like version of Pipeline 2 Feature Engineering and provides the materialized dataset artifact required for future Pipeline 3 ML training.
