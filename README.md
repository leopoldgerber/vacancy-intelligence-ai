# Pipeline 1: Data Validation, Quality Checks and Ingestion

## Overview

Pipeline 1 is responsible for checking and loading prepared vacancy data into
PostgreSQL.

It represents the first production-style data flow in the project:

1. Accept an uploaded `.xlsx` file through the API.
2. Run data validation.
3. Run data quality checks.
4. Decide whether the file can be ingested.
5. Load validated data into PostgreSQL.
6. Save validation and quality results.
7. Generate `.md` reports.
8. Handle repeated uploads safely.

The pipeline is designed as an engineering MVP: it is simple enough for a
portfolio project, but structured as a real backend/data system component.

---

## Pipeline Goal

The goal of Pipeline 1 is to ensure that only structurally valid and technically
checked data reaches the ingestion layer.

The pipeline answers three main questions:

- Is the uploaded file valid enough to process?
- What technical issues were found in the dataset?
- What data should be inserted or updated in the database?

If blocking validation errors are found, ingestion is not executed.

---

## High-Level Flow

```text
.xlsx upload
    ↓
API endpoint
    ↓
file extension and read checks
    ↓
DataFrame creation
    ↓
data validation
    ↓
data quality checks
    ↓
pre-ingestion decision
    ↓
ingestion pipeline
    ↓
PostgreSQL
    ↓
.md reports
```

---

## Main Components

### API Layer

The API layer accepts files, validates request-level requirements and returns
pipeline execution results.

Implemented endpoints:

```text
GET  /health
POST /clients
POST /validation/upload
POST /pipeline/run
```

Main modules:

```text
app/api/main.py
app/api/routes/health.py
app/api/routes/clients.py
app/api/routes/validation.py
app/api/routes/pipeline.py
app/api/schemas/client.py
app/api/schemas/validation.py
app/api/schemas/pipeline.py
app/api/exception_handlers.py
```

---

### Data Validation Layer

The validation layer checks whether the uploaded dataset satisfies the required
contract.

It includes:

- dataset structure checks;
- required column checks;
- empty dataset check;
- critical field type checks;
- datetime format checks;
- reference check for `client_id` against the `clients` table;
- blocking error aggregation;
- validation result persistence;
- validation report generation.

Main modules:

```text
app/services/data_validation/constants.py
app/services/data_validation/schema_checks.py
app/services/data_validation/field_checks.py
app/services/data_validation/result_builders.py
app/services/data_validation/run_validation.py
app/services/data_validation/run_validation_pipeline.py
app/services/data_validation/persistence.py
app/services/data_validation/repositories.py
app/services/data_validation/report_builders.py
app/services/data_validation/service.py
```

Validation results are saved to:

```text
validation_runs
validation_issues
```

---

### Data Quality Layer

The quality layer does not block ingestion by itself. It records technical
quality issues that are useful for analysis and reporting.

It includes:

- sample size check;
- missing values check;
- duplicate rows check;
- empty text values check;
- whitespace-only text values check;
- quality summary generation;
- quality result persistence;
- quality report generation.

Main modules:

```text
app/services/data_quality/checks.py
app/services/data_quality/result_builders.py
app/services/data_quality/repositories.py
app/services/data_quality/persistence.py
app/services/data_quality/report_builders.py
app/services/data_quality/run_quality_pipeline.py
app/services/data_quality/service.py
```

Quality results are saved to:

```text
quality_runs
quality_issues
```

---

### Pre-Ingestion Layer

The pre-ingestion layer connects validation and quality checks into one decision
step before data loading.

Logic:

1. Run validation.
2. If validation fails, stop the pipeline.
3. If validation succeeds, run quality checks.
4. Return the decision whether ingestion should continue.

Main modules:

```text
app/services/pre_ingestion/run_pre_ingestion_pipeline.py
app/services/pre_ingestion/service.py
```

---

### Ingestion Layer

The ingestion layer writes validated vacancy data into PostgreSQL.

It includes:

- automatic company upsert;
- vacancy upsert;
- vacancy snapshot insert;
- duplicate snapshot protection;
- idempotent repeated file upload handling.

Main modules:

```text
app/services/ingestion/companies/parsers.py
app/services/ingestion/companies/repositories.py
app/services/ingestion/companies/service.py
app/services/ingestion/vacancies/parsers.py
app/services/ingestion/vacancies/repositories.py
app/services/ingestion/vacancies/service.py
app/services/ingestion/vacancy_snapshots/parsers.py
app/services/ingestion/vacancy_snapshots/repositories.py
app/services/ingestion/vacancy_snapshots/service.py
app/services/ingestion/run_ingestion_pipeline.py
app/services/ingestion/service.py
```

Ingestion data is saved to:

```text
companies
vacancies
vacancy_snapshots
```

---

### Full Pipeline Layer

The full pipeline layer combines pre-ingestion and ingestion into one executable
business flow.

Main modules:

```text
app/services/pipeline/run_pipeline_1.py
app/services/pipeline/service.py
```

The expected successful response has the following structure:

```json
{
  "status": "ok",
  "message": "Pipeline 1 completed successfully.",
  "should_ingest": true,
  "company_count": 3,
  "vacancy_count": 1363,
  "snapshot_count": 17145
}
```

---

## Database Tables

### `clients`

Stores client reference data.

Purpose:

- validate that `client_id` from the uploaded file exists;
- support client-scoped company mapping.

Main fields:

```text
id
name
is_active
created_at
```

---

### `validation_runs`

Stores one validation execution record.

Purpose:

- track validation execution status;
- store high-level validation metadata;
- link validation results with generated reports.

---

### `validation_issues`

Stores aggregated validation issues for one validation run.

Purpose:

- store blocking validation issue counts;
- keep the report content aligned with database records.

---

### `quality_runs`

Stores one data quality execution record.

Purpose:

- track quality check execution status;
- store high-level quality metadata;
- link quality results with generated reports.

---

### `quality_issues`

Stores aggregated quality issues for one quality run.

Purpose:

- store warning-level issue counts;
- keep quality reports based only on persisted results.

---

### `companies`

Stores companies related to a specific client.

Uniqueness rule:

```text
client_id + name
```

This allows the same company name to exist for different clients.

---

### `vacancies`

Stores the latest known state of each vacancy.

Key decision:

```text
vacancy_id from the source is used as the primary key.
```

The table is used for the current vacancy state, not historical snapshots.

---

### `vacancy_snapshots`

Stores historical daily vacancy snapshots.

Duplicate protection key:

```text
client_id
company_id
vacancy_id
date_day
```

This prevents repeated uploads of the same file from creating duplicate history
records.

---

## Reports

Pipeline 1 generates `.md` reports for validation and quality checks.

Report content is intentionally limited to the same information that is saved in
PostgreSQL. This keeps reports reproducible and prevents divergence between the
file output and database state.

Report names use the operation timestamp format:

```text
validation_YYYY-MM-DD_HH-MM-SS.md
quality_YYYY-MM-DD_HH-MM-SS.md
```

---

## Error Handling

The pipeline uses domain-level exceptions and a centralized FastAPI exception
handler.

Implemented error types include:

```text
MissingFileNameError
InvalidFileExtensionError
FileReadError
ValidationExecutionError
PipelineExecutionError
CompanyMappingError
VacancyIngestionError
VacancySnapshotIngestionError
```

Expected errors return controlled API responses instead of raw internal server
errors.

---

## Idempotency

Repeated upload of the same already ingested file is safe.

Expected behavior:

- companies are not duplicated;
- vacancies are updated or kept as-is;
- identical vacancy snapshots are not inserted again;
- the pipeline returns `snapshot_count = 0` for already existing snapshots.

This makes the ingestion flow safe for manual retries and repeated local tests.

---

## Tests

Pipeline 1 is covered by API tests and unit tests.

### API Tests

```text
tests/api/test_pipeline_success.py
tests/api/test_pipeline_errors.py
tests/api/test_clients_success.py
tests/api/test_clients_errors.py
tests/api/pipeline_helpers.py
```

Covered scenarios include:

- successful pipeline execution;
- repeated file upload;
- invalid file extension;
- missing or invalid client reference;
- client creation;
- duplicate client creation.

### Unit Tests

```text
tests/unit/test_schema_checks.py
tests/unit/test_field_checks.py
tests/unit/test_validation_result_builders.py
tests/unit/test_data_quality_checks.py
tests/unit/test_data_quality_result_builders.py
tests/unit/test_ingestion_parsers.py
tests/unit/test_ingestion_companies.py
tests/unit/test_ingestion_vacancies.py
tests/unit/test_ingestion_vacancy_snapshots.py
```

Covered areas include:

- schema checks;
- field checks;
- validation result builders;
- quality checks;
- quality result builders;
- ingestion parsers;
- company helpers;
- vacancy helpers;
- snapshot key helpers.

---

## Makefile Commands

### Database

```bash
make db-up
make db-down
make db-logs
```

### API

```bash
make api-run
make api-health
```

### Tests

```bash
make test
make test-api
make test-unit
```

---

## Current Status

Pipeline 1 is complete at the engineering MVP level.

Completed:

- `.xlsx` upload through API;
- validation layer;
- quality layer;
- pre-ingestion decision layer;
- PostgreSQL ingestion;
- validation and quality persistence;
- `.md` report generation;
- repeated upload protection;
- expected error handling;
- API tests;
- unit tests;
- Makefile test commands.

Pipeline 1 can be considered ready as the foundation for the next stage:

```text
Pipeline 2: Analytics and Feature Engineering
```

---

## Future Improvements

Planned or possible improvements after Pipeline 1:

- add structured logging;
- extend API response details;
- add integration tests with a dedicated test database;
- add CI test execution;
- improve validation issue detail storage if needed;
- add analytics tables in Pipeline 2;
- add aggregated vacancy metrics later;
- add async background processing when API workload grows.
