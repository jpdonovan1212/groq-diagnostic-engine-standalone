.PHONY: up down logs build test clean help

UP = docker compose up -d
DOWN = docker compose down
LOGS = docker compose logs -f --tail=100
BUILD = docker compose build
TEST = pytest -v --tb=short
CLEAN = docker compose down --rmi local --volumes --remove-orphans

help:
	@echo "Available commands:"
	@echo "  make up      - Start services in detached mode"
	@echo "  make down    - Stop and remove containers, networks"
	@echo "  make logs    - Follow logs for all services"
	@echo "  make build   - Build/rebuild images"
	@echo "  make test    - Run tests with verbose output"
	@echo "  make clean   - Remove containers, images, volumes"

up:
	$(UP)

down:
	$(DOWN)

logs:
	$(LOGS)

build:
	$(BUILD)

test:
	$(TEST)

clean:
	$(CLEAN)
