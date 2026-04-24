# Database
COMPOSE_POSTGRES_FILE = infra/compose/docker-compose.postgres.yml

db-up:
	docker compose -f $(COMPOSE_POSTGRES_FILE) --env-file .env up -d

db-down:
	docker compose -f $(COMPOSE_POSTGRES_FILE) --env-file .env down

db-logs:
	docker compose -f $(COMPOSE_POSTGRES_FILE) --env-file .env logs -f postgres


