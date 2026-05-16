# Pipeline 2 - Full Run

## Purpose

The Pipeline 2 Full Run provides a single orchestration endpoint for the complete Pipeline 2 flow. It executes the analytics summary layer, all implemented feature engineering layers, and the final materialized ML dataset build in a fixed order.

This layer is intended to make Pipeline 2 usable as an end-to-end production-like process, while keeping the internal components modular and independently testable.

## Endpoint

```text
POST /pipeline-2/run
```

## Inputs

The endpoint accepts form-data fields:

```text
client_id
date_from
date_to
```

Default values used for local testing:

```text
client_id = 1
date_from = 2025-08-01
date_to = 2025-08-21
```

## Execution Order

The full run executes the following steps in sequence:

```text
1. Analytics Summary
2. Salary Features
3. Publication Activity Features
4. Text Features
5. Time Features
6. Categorical Features
7. ML Dataset
```

## Components

### Analytics Summary

Runs the summary analytics layer and creates:

```text
analytics_runs
market_summaries
client_summaries
competitor_summaries
```

The summary layer provides high-level market, client, and competitor overview metrics.

### Salary Features

Runs salary feature engineering and creates rows in:

```text
salary_features
```

This layer calculates row-level salary signals and leave-one-company-out market salary ratios.

### Publication Activity Features

Runs publication activity feature engineering and creates rows in:

```text
publication_activity_features
```

This layer uses `standard`, `standard_plus`, and `premium` as publication activity indicators, not as static vacancy tariff labels.

### Text Features

Runs text feature engineering and creates rows in:

```text
text_features
```

This layer calculates explainable text-based features from vacancy title and description. Embeddings are intentionally not included in this layer.

### Time Features

Runs time feature engineering and creates rows in:

```text
time_features
```

This layer extracts publication time and vacancy age features from `publication_date` and `date_day`.

### Categorical Features

Runs categorical feature engineering and creates rows in:

```text
categorical_features
```

This layer stores normalized business categories such as city, region, profile, employment type, work experience, and work schedule.

### ML Dataset

Runs the final materialized ML dataset build and creates:

```text
ml_dataset_runs
ml_feature_rows
```

The ML dataset layer joins all feature layers by:

```text
client_id
company_id
vacancy_id
date_day
```

It stores concrete feature values rather than only references to feature rows. This makes each ML dataset run reproducible and suitable as an input artifact for Pipeline 3.

## Response Structure

The full run response contains the result of every sub-step:

```text
status
is_success
summary
salary_features
publication_activity_features
text_features
time_features
categorical_features
ml_dataset
```

A successful run returns:

```text
status = success
is_success = true
```

If one or more sub-steps have no data, the response returns:

```text
status = partial_or_no_data
is_success = false
```

## Makefile Command

The Makefile includes:

```makefile
pipeline-2:
	curl -X POST http://127.0.0.1:8000/pipeline-2/run \
		-F "client_id=1" \
		-F "date_from=2025-08-01" \
		-F "date_to=2025-08-21"
```

The local setup command can call Pipeline 2 through the full-run endpoint after creating the client and running Pipeline 1.

## Testing

The full run is covered by API tests:

```text
tests/api/test_pipeline_2_full_run_success.py
tests/api/test_pipeline_2_full_run_errors.py
```

The success test verifies that:

```text
- the full endpoint returns HTTP 200
- the overall status is success
- the summary run is created
- all five feature runs are created
- all feature tables are populated
- the ML dataset run is created
- ML feature rows are materialized
```

The no-data test verifies that:

```text
- the endpoint returns HTTP 200
- the overall status is partial_or_no_data
- all sub-steps return no_data where appropriate
- no feature rows are created
- the ML dataset run is created with row_count = 0
```

## Architecture Notes

Pipeline 2 is intentionally split into separate internal layers:

```text
Analytics Summary
Feature Layers
Materialized ML Dataset
```

This separation keeps reporting logic, feature engineering logic, and final ML dataset materialization independent and testable.

The full-run endpoint does not replace the individual endpoints. Individual endpoints remain useful for debugging, partial recomputation, and targeted development.

## Current Limitations

The full run assumes that Pipeline 1 has already populated `vacancy_snapshots` for the selected client and period.

The ML dataset layer uses the latest successful feature runs for each feature group and matching period. Feature run names are therefore prefixed by feature group names such as:

```text
salary_features_
publication_activity_features_
text_features_
time_features_
categorical_features_
```

This naming convention is required for the ML dataset builder to select the correct feature runs.

## Next Step

Pipeline 2 now produces a materialized ML-ready dataset in `ml_feature_rows`.

The next major project stage is Pipeline 3:

```text
ML Training
```

Pipeline 3 should use `ml_dataset_runs` and `ml_feature_rows` as its primary input source.
