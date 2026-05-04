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

# Tests
test:
	uv run pytest

test-api:
	uv run pytest tests/api

test-unit:
	uv run pytest tests/unit

