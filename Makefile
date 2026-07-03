# Database
COMPOSE_POSTGRES_FILE = infra/compose/docker-compose.postgres.yml

db-up:
	docker compose -f $(COMPOSE_POSTGRES_FILE) --env-file .env up -d

db-down:
	docker compose -f $(COMPOSE_POSTGRES_FILE) --env-file .env down

db-logs:
	docker compose -f $(COMPOSE_POSTGRES_FILE) --env-file .env logs -f postgres

# Migrations
db-migrate:
	uv run alembic upgrade head

# Server
api-run:
	uv run uvicorn app.api.main:app --reload

api-health:
	curl http://127.0.0.1:8000/health

# Clients
CLIENT_ID ?= 1
CLIENT_NAME ?= company_1
CLIENT_IS_ACTIVE ?= true

client-create:
	curl -X POST http://127.0.0.1:8000/clients \
		-H "Content-Type: application/json" \
		-d '{"client_id":$(CLIENT_ID),"name":"$(CLIENT_NAME)","is_active":$(CLIENT_IS_ACTIVE)}'

# Pipeline 1
INPUT_FILE ?= data/input_sample.xlsx

pipeline-1:
	curl -X POST http://127.0.0.1:8000/pipeline-1/run \
		-F "file=@$(INPUT_FILE)"

# Pipeline 2 - Summary Analytics
pipeline-2-summary:
	curl -X POST http://127.0.0.1:8000/pipeline-2/analytics/summary/run \
		-F "client_id=1" \
		-F "date_from=2025-08-01" \
		-F "date_to=2025-08-21" \
		-F "city=" \
		-F "profile="

# Pipeline 2 - Salary Features
pipeline-2-salary-features:
	curl -X POST http://127.0.0.1:8000/pipeline-2/features/salary/run \
		-F "client_id=1" \
		-F "date_from=2025-08-01" \
		-F "date_to=2025-08-21"

# Pipeline 2 - Publication Activity Features
pipeline-2-publication-activity-features:
	curl -X POST http://127.0.0.1:8000/pipeline-2/features/publication-activity/run \
		-F "client_id=1" \
		-F "date_from=2025-08-01" \
		-F "date_to=2025-08-21"

# Pipeline 2 - Text Features
pipeline-2-text-features:
	curl -X POST http://127.0.0.1:8000/pipeline-2/features/text/run \
		-F "client_id=1" \
		-F "date_from=2025-08-01" \
		-F "date_to=2025-08-21"

# Pipeline 2 - Time Features
pipeline-2-time-features:
	curl -X POST http://127.0.0.1:8000/pipeline-2/features/time/run \
		-F "client_id=1" \
		-F "date_from=2025-08-01" \
		-F "date_to=2025-08-21"

# Pipeline 2 - Categorical Features
pipeline-2-categorical-features:
	curl -X POST http://127.0.0.1:8000/pipeline-2/features/categorical/run \
		-F "client_id=1" \
		-F "date_from=2025-08-01" \
		-F "date_to=2025-08-21"

# Pipeline 2 - ML Dataset
pipeline-2-ml-dataset:
	curl -X POST http://127.0.0.1:8000/pipeline-2/ml-dataset/run \
		-F "client_id=1" \
		-F "date_from=2025-08-01" \
		-F "date_to=2025-08-21"

# Pipeline 2 - Full Run
pipeline-2:
	curl -X POST http://127.0.0.1:8000/pipeline-2/run \
		-F "client_id=1" \
		-F "date_from=2025-08-01" \
		-F "date_to=2025-08-21"

# Pipeline 3 - ML Training
pipeline-3-training:
	curl -X POST http://127.0.0.1:8000/pipeline-3/training/run \
		-F "client_id=1" \
		-F "ml_dataset_run_id="

# Pipeline 3 - ML Inference
ML_TRAINING_RUN_ID ?=

pipeline-3-inference:
	@if [ -z "$(ML_TRAINING_RUN_ID)" ]; then \
		curl -X POST http://127.0.0.1:8000/pipeline-3/inference/run \
			-H "Content-Type: application/json" \
			-d '{"client_id":$(CLIENT_ID)}'; \
	else \
		curl -X POST http://127.0.0.1:8000/pipeline-3/inference/run \
			-H "Content-Type: application/json" \
			-d '{"client_id":$(CLIENT_ID),"ml_training_run_id":$(ML_TRAINING_RUN_ID)}'; \
	fi

# Full local data setup
local-data-setup:
	$(MAKE) client-create
	$(MAKE) pipeline-1
	$(MAKE) pipeline-2-summary
	$(MAKE) pipeline-2-salary-features
	$(MAKE) pipeline-2-publication-activity-features
	$(MAKE) pipeline-2-text-features
	$(MAKE) pipeline-2-time-features
	$(MAKE) pipeline-2-categorical-features
	$(MAKE) pipeline-2-ml-dataset

# Pipeline 1 + Pipeline 2 + Pipeline 3 local setup
local-ml-setup:
	$(MAKE) local-data-setup
	$(MAKE) pipeline-3-training

# Tests
test:
	uv run pytest

test-api:
	uv run pytest tests/api

test-unit:
	uv run pytest tests/unit
