.PHONY: help install dev test lint format migrate up down

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make dev        - Start development server"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linters"
	@echo "  make format     - Format code with black"
	@echo "  make migrate    - Create new migration"
	@echo "  make upgrade    - Apply migrations"
	@echo "  make up         - Start Docker services"
	@echo "  make down       - Stop Docker services"

install:
	pip install -e ".[dev]"

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest

lint:
	flake8 app
	mypy app

format:
	black app

migrate:
	alembic revision --autogenerate -m "$(msg)"

upgrade:
	alembic upgrade head

up:
	docker-compose up -d

down:
	docker-compose down



