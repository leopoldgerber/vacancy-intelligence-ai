# Database
COMPOSE_POSTGRES_FILE = infra/compose/docker-compose.postgres.yml

db-up:
	docker compose -f $(COMPOSE_POSTGRES_FILE) --env-file .env up -d

db-down:
	docker compose -f $(COMPOSE_POSTGRES_FILE) --env-file .env down

db-logs:
	docker compose -f $(COMPOSE_POSTGRES_FILE) --env-file .env logs -f postgres

# Server
api-run:
	uv run uvicorn app.api.main:app --reload

api-health:
	curl http://127.0.0.1:8000/health