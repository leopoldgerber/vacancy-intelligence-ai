# Pipeline 2: Text Features

## Overview

The Text Features layer is part of Pipeline 2 Feature Engineering.

It extracts simple, explainable and model-friendly features from vacancy titles
and vacancy descriptions. This layer intentionally does not create text
embeddings. The goal is to provide stable baseline text signals that can be
used by classical ML models such as CatBoost, XGBoost or ensemble models.

Text semantic analysis and embedding-based features are reserved for later AI
context or semantic feature layers.

---

## Feature Layer Goal

The goal of the Text Features layer is to convert raw vacancy text fields into
structured numeric and boolean features.

The layer answers questions such as:

- How long is the vacancy title?
- How long is the vacancy description?
- Is the description missing?
- Does the text mention salary?
- Does the text mention schedule or working time?
- Does the text contain requirements?
- Does the text mention benefits?
- Does the text include a call to action?

These features are intentionally simple, transparent and easy to validate.

---

## Input Data

The layer uses vacancy snapshot data loaded from PostgreSQL.

Main source table:

```text
vacancy_snapshots
```

Main input fields:

```text
client_id
company_id
vacancy_id
date_day
vacancy_title
vacancy_description
```

The shared feature data loader was extended to include:

```text
vacancy_title
vacancy_description
```

---

## Output Table

Text features are saved to:

```text
text_features
```

Each row represents one vacancy snapshot within one feature engineering run.

Granularity:

```text
feature_run_id + client_id + company_id + vacancy_id + date_day
```

A unique constraint prevents duplicate feature rows for the same snapshot within
one feature run.

---

## Database Fields

The `text_features` table contains:

```text
id
feature_run_id
client_id
company_id
vacancy_id
date_day
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
created_at
```

---

## Feature Definitions

### `title_length`

Number of characters in the cleaned vacancy title.

If the title is missing or empty, the value is `0`.

### `description_length`

Number of characters in the cleaned vacancy description.

If the description is missing or empty, the value is `0`.

### `title_word_count`

Number of words in the cleaned vacancy title.

### `description_word_count`

Number of words in the cleaned vacancy description.

### `has_description`

Boolean flag indicating whether the vacancy has a non-empty description.

### `description_is_empty`

Boolean flag indicating whether the vacancy description is missing or empty.

### `has_salary_mention`

Boolean flag indicating whether the title or description contains salary-related
terms.

### `has_schedule_mention`

Boolean flag indicating whether the title or description contains working time,
schedule, shift or remote-work related terms.

### `has_requirements_mention`

Boolean flag indicating whether the title or description contains requirement-
related terms.

### `has_benefits_mention`

Boolean flag indicating whether the title or description contains benefit- or
employer-offer-related terms.

### `has_call_to_action`

Boolean flag indicating whether the title or description contains application or
call-to-action wording.

---

## Keyword-Based Rules

The current implementation uses deterministic keyword matching.

Keyword groups include:

```text
salary keywords
schedule keywords
requirements keywords
benefits keywords
call-to-action keywords
```

The keyword logic is intentionally implemented in code instead of being loaded
from an external spreadsheet at runtime. This keeps the feature layer
reproducible and version-controlled.

The uploaded unique text samples can be used later to improve and extend keyword
lists.

---

## Text Cleaning

Text is cleaned before feature calculation.

Cleaning rules:

- convert missing values to empty strings;
- strip leading and trailing whitespace;
- collapse repeated whitespace into a single space.

Keyword search uses a combined text field:

```text
cleaned_title + cleaned_description
```

The search is case-insensitive.

---

## Embeddings Decision

Text embeddings are intentionally not implemented in this layer.

Reasoning:

- the current ML direction is based on classical models such as CatBoost,
  XGBoost and ensembles;
- raw embeddings are high-dimensional numeric vectors and are not always useful
  for tree-based models without additional processing;
- embedding-based features require separate design decisions around model
  choice, vector storage, dimensionality reduction, clustering and similarity
  features;
- semantic text analysis is more relevant for later AI context and insight
  generation.

Future text semantic work may include:

```text
text embeddings
text clusters
similarity to high-performing vacancies
similarity to market-best vacancy texts
semantic text quality signals
AI-context text summaries
```

These are intentionally left out of the current Text Features layer.

---

## Main Components

### Database Model

```text
app/db/models/text_feature.py
```

### Feature Builder

```text
app/services/features/text_feature_builders.py
```

### Pipeline Runner

```text
app/services/features/run_text_features_pipeline.py
```

### Service Layer

```text
app/services/features/service.py
```

### API Route

```text
app/api/routes/features.py
```

### Shared Feature Loader

```text
app/services/features/data_loaders.py
```

---

## API Endpoint

The Text Features layer can be executed through:

```text
POST /pipeline-2/features/text/run
```

Form fields:

```text
client_id
date_from
date_to
```

The feature run processes all vacancy snapshots for the selected client and date
range.

---

## Makefile Command

The following Makefile command was added:

```bash
make pipeline-2-text-features
```

It calls:

```text
POST /pipeline-2/features/text/run
```

with the default local development values.

The text feature step is also included in the local data rebuild command:

```bash
make local-data-setup
```

---

## Tests

The Text Features layer is covered by unit and API tests.

### Unit Tests

```text
tests/unit/test_text_feature_builders.py
```

Covered logic:

- text cleaning;
- word counting;
- keyword detection;
- feature dataframe construction;
- feature row construction;
- empty input handling.

### API Tests

```text
tests/api/test_pipeline_2_text_features_success.py
tests/api/test_pipeline_2_text_features_errors.py
```

Covered scenarios:

- successful text feature run;
- `feature_runs` persistence;
- `text_features` persistence;
- correct feature count;
- basic text length and word count checks;
- keyword flag checks;
- no-data scenario.

---

## Current Status

The Text Features layer is complete at the current production-like project stage.

Completed:

- `text_features` table;
- SQLAlchemy model;
- Alembic migration;
- feature data loader extension;
- text feature builder;
- persistence function;
- pipeline runner;
- service wrapper;
- API endpoint;
- Makefile command;
- unit tests;
- API tests.

The layer is ready to be used as one of the feature sources for the future final
feature dataset and Pipeline 3 ML training.

---

## Future Improvements

Possible future improvements:

- expand keyword lists using real vacancy text samples;
- add language-specific keyword variants;
- add normalized text length features;
- add title-to-description ratio features;
- add text quality score;
- add semantic text features for AI context;
- add embeddings, clustering or similarity features in a separate semantic text
  layer;
- validate which text signals improve ML performance during model evaluation.
