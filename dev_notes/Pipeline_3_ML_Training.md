# Pipeline 3 - ML Training

## Purpose

Pipeline 3 implements the first ML training layer for the vacancy intelligence system.

Its purpose is to train a regression model that predicts the number of vacancy callbacks using the materialized ML-ready dataset created by Pipeline 2.

Pipeline 3 does not recalculate feature engineering layers. It uses the already materialized rows from `ml_feature_rows`.

---

## Position in the Project

The current project flow is:

```text
Pipeline 1 -> Data import / validation / normalization / DB persistence
Pipeline 2 -> Analytics Summary + Feature Engineering + ML Dataset materialization
Pipeline 3 -> ML Training, evaluation, model artifact persistence
Future -> AI Context, Recommendations, Model-based simulations
```

Pipeline 3 starts after Pipeline 2 has successfully created an ML dataset run and populated `ml_feature_rows`.

---

## Input Data

Pipeline 3 uses:

```text
ml_dataset_runs
ml_feature_rows
```

The training endpoint can work in two modes:

1. Use a specific `ml_dataset_run_id`.
2. If `ml_dataset_run_id` is not provided, load the latest successful ML dataset run for the given `client_id`.

Pipeline 3 deliberately avoids joining raw feature tables during training. This keeps training reproducible and tied to one exact materialized dataset snapshot.

---

## Target

The current target is:

```text
callbacks
```

This is treated as a regression target.

The first ML task is:

```text
Predict the expected number of callbacks for vacancy snapshots.
```

---

## Model

The first implemented model is:

```text
CatBoostRegressor
```

Reasons for this choice:

- suitable for tabular data;
- supports categorical features directly;
- requires less preprocessing than many other gradient boosting models;
- fits the current feature dataset design;
- provides a practical production-like baseline.

The model is currently trained with fixed baseline hyperparameters in code.

Current baseline parameters:

```text
iterations = 100
learning_rate = 0.05
depth = 6
loss_function = RMSE
random_seed = 42
verbose = False
allow_writing_files = False
```

Hyperparameter tuning is intentionally not implemented in the first version.

---

## Feature Schema

Pipeline 3 defines an explicit feature schema.

Identifier columns:

```text
client_id
company_id
vacancy_id
date_day
```

These columns are used for traceability and splitting logic, but they are not model features.

Target column:

```text
callbacks
```

Numerical and binary feature columns:

```text
salary_mid
salary_is_specified
salary_ratio_to_market_by_city
salary_ratio_to_market_by_profile
salary_ratio_to_market_by_city_profile
publication_activity_level
days_since_last_publication_activity
title_length
description_length
title_word_count
description_word_count
has_description
description_is_empty
has_salary_mention
has_schedule_mention
has_requirements_mention
has_benefits_mention
has_call_to_action
publication_hour
publication_day_of_week
publication_month
publication_week
is_weekend
vacancy_age_days
```

Categorical feature columns:

```text
city
region
profile
employment_type
work_experience
work_schedule
```

CatBoost receives categorical feature indices derived from this schema.

---

## Dataset Preparation

Pipeline 3 validates the training dataframe before model fitting.

Validation includes:

- required columns exist;
- dataframe is not empty;
- row count is sufficient;
- target column has no missing values;
- target can be converted to numeric values.

Feature normalization rules:

- numerical features are converted to numeric and missing values are filled with `0`;
- categorical features are converted to string;
- missing or empty categorical values are replaced with `unknown`.

Minimum row count for training is currently:

```text
10
```

---

## Train/Test Split

Pipeline 3 implements a reusable split builder.

Preferred split strategy:

```text
time_based
```

If the dataset has at least two unique `date_day` values, the latest date segment is used as the test set.

Fallback strategy:

```text
random_fallback
```

If there are not enough unique dates, deterministic `train_test_split` is used with:

```text
random_seed = 42
test_size = 0.2
```

---

## Metrics

Pipeline 3 calculates the following model metrics:

```text
MAE
RMSE
R2
```

It also calculates supporting baseline values in the metric builder:

```text
baseline_mae
mean_target
```

The database table currently stores:

```text
metric_mae
metric_rmse
metric_r2
```

The baseline metrics are calculated internally but are not yet stored in `ml_training_runs`.

---

## Model Artifacts

CatBoost models are saved as `.cbm` files.

Artifact directory:

```text
artifacts/models/pipeline_3
```

Example artifact path:

```text
artifacts/models/pipeline_3/ml_training_2026-05-17_21-52-56.cbm
```

The model file is not stored in the database.

The database stores only the artifact path:

```text
ml_training_runs.model_path
```

---

## Training Reports

Pipeline 3 creates a Markdown report for each training run.

Report directory:

```text
artifacts/reports/pipeline_3/training
```

Example report name:

```text
ml_training_2026-05-17_21-52-56.md
```

The report documents:

- run metadata;
- dataset run ID;
- client ID;
- model type;
- target;
- train/test row counts;
- metrics;
- model artifact path.

---

## Database Table

Pipeline 3 added the table:

```text
ml_training_runs
```

Purpose:

```text
Store metadata for each ML training execution.
```

Fields:

```text
id
training_run_name
ml_dataset_run_id
client_id
model_type
target_name
status
is_success
train_row_count
test_row_count
metric_mae
metric_rmse
metric_r2
model_path
report_name
created_at
```

`ml_dataset_run_id` is nullable so failed or no-data training attempts can still be recorded.

---

## Status Values

Pipeline 3 currently uses these statuses:

```text
success
failed
no_data
```

Meaning:

```text
success -> model training completed successfully
failed  -> expected training validation/preparation failure
no_data -> no usable dataset was found or not enough rows were available
```

---

## Endpoint

Pipeline 3 exposes the endpoint:

```http
POST /pipeline-3/training/run
```

Input form fields:

```text
client_id
ml_dataset_run_id optional
```

If `ml_dataset_run_id` is empty, Pipeline 3 uses the latest successful ML dataset run for the given client.

Response fields:

```text
ml_training_run_id
training_run_name
status
is_success
model_type
target_name
train_row_count
test_row_count
metric_mae
metric_rmse
metric_r2
model_path
report_name
```

---

## Makefile Command

Pipeline 3 added:

```makefile
pipeline-3-training:
	curl -X POST http://127.0.0.1:8000/pipeline-3/training/run \
		-F "client_id=1" \
		-F "ml_dataset_run_id="
```

A helper command was also added:

```makefile
local-ml-setup:
	$(MAKE) local-data-setup
	$(MAKE) pipeline-3-training
```

---

## Tests

Pipeline 3 added unit tests for:

- feature schema;
- dataset builder;
- train/test split builder;
- metric builder;
- CatBoost model builder;
- model artifact saver;
- training run name builder;
- training report builder.

Pipeline 3 also added API tests for:

- successful training endpoint response;
- training endpoint with explicit `ml_dataset_run_id`;
- no-data training endpoint response.

API tests mock the ML training service to avoid training CatBoost during normal API test execution.

---

## Known Test Environment Limitation

API tests currently use the configured real database through the existing test setup.

The test cleanup function deletes rows from project tables. Therefore, running API tests can remove local development data.

After tests, development data can be recreated with:

```bash
make local-data-setup
```

or including Pipeline 3:

```bash
make local-ml-setup
```

The cleanup order was updated to include:

```text
ml_training_runs
```

before deleting `ml_feature_rows` and `ml_dataset_runs`.

Recommended future improvement:

```text
Use a separate TEST_DATABASE_URL and isolated test database.
```

---

## Current Limitations

Pipeline 3 currently does not implement:

- hyperparameter tuning;
- cross-validation;
- model comparison;
- model registry beyond artifact path persistence;
- prediction/inference endpoint;
- prediction result storage;
- recommendation logic;
- AI insights;
- simulation or evaluation beyond basic metrics.

The current model quality is accepted as a baseline. The first goal was to make the ML training flow reproducible, testable, and connected to the materialized Pipeline 2 dataset.

---

## Current Working State

At this stage:

- Pipeline 3 can train a CatBoostRegressor from `ml_feature_rows`;
- model artifacts are saved as `.cbm` files;
- training metadata is saved in `ml_training_runs`;
- Markdown training reports are generated;
- API endpoint works;
- Makefile command works;
- tests for Pipeline 3 components pass.

Pipeline 3 is now implemented as the first production-like ML training layer.
