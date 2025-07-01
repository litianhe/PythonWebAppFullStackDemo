.PHONY: venv install install-dev migrate run test lint format docker

UV ?= uv
SHELL := /bin/bash

venv:
	cd backend && \
	$(UV) venv

install:
	cd backend && \
	source .venv/bin/activate && \
	$(UV) sync --no-dev

install-dev:
	cd backend && \
	source .venv/bin/activate && \
	$(UV) sync --extra dev

db: venv install
	cd backend && \
	source .venv/bin/activate && \
	$(UV) run scripts/migrate_db.py && \
	alembic upgrade head



run: venv install migrate
	cd backend && \
	source .venv/bin/activate && \
	./scripts/start_app.sh

test: venv install-dev
	cd backend && \
	source .venv/bin/activate && \
	python -m pytest -xv tests/ . -s

lint: venv install-dev
	cd backend && \
	source .venv/bin/activate && \
	ruff check app/
	cd backend && \
	source .venv/bin/activate && \
	. .venv/bin/activate && mypy app/

format: venv install-dev
	cd backend && \
	source .venv/bin/activate && \
	black app/
	cd backend && \
	source .venv/bin/activate && \
	isort app/


docker:
	cd backend && \
	sudo docker build -t comment-app:v0.0.1 -f Dockerfile .