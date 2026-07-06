.PHONY: help \
        install install-backend install-frontend \
        dev-backend dev-frontend \
        play \
        lint lint-backend lint-frontend \
        format format-backend format-frontend \
        typecheck \
        test test-backend test-frontend \
        test-integration test-coverage \
        docker-build docker-up docker-down docker-logs \
        k8s-apply k8s-delete k8s-status \
        clean

# ── Default target ────────────────────────────────────────────────────────────
help:
	@echo ""
	@echo "Block Blast — available commands:"
	@echo ""
	@echo "  Quick Start"
	@echo "    make play               Start the full game (Docker)"
	@echo ""
	@echo "  Setup"
	@echo "    make install            Install all dependencies (backend + frontend)"
	@echo "    make install-backend    Install backend dependencies"
	@echo "    make install-frontend   Install frontend dependencies"
	@echo ""
	@echo "  Development"
	@echo "    make dev-backend        Start backend dev server (uvicorn)"
	@echo "    make dev-frontend       Start frontend dev server (vite)"
	@echo ""
	@echo "  Lint & Format"
	@echo "    make lint               Lint backend and frontend"
	@echo "    make lint-backend       Ruff lint check"
	@echo "    make lint-frontend      ESLint check"
	@echo "    make format             Format backend and frontend"
	@echo "    make format-backend     Ruff format"
	@echo "    make format-frontend    Prettier format"
	@echo "    make typecheck          Pyrefly type check (backend)"
	@echo ""
	@echo "  Tests"
	@echo "    make test               Run all unit tests (backend + frontend)"
	@echo "    make test-backend       Backend unit tests only"
	@echo "    make test-frontend      Frontend tests only"
	@echo "    make test-integration   Backend integration tests (requires Docker)"
	@echo "    make test-coverage      Run all tests with coverage reports"
	@echo ""
	@echo "  Docker"
	@echo "    make docker-build       Build all Docker images"
	@echo "    make docker-up          Start all services via docker compose"
	@echo "    make docker-down        Stop all services"
	@echo "    make docker-logs        Tail logs from all services"
	@echo ""
	@echo "  Kubernetes"
	@echo "    make k8s-apply          Apply all manifests to the cluster"
	@echo "    make k8s-delete         Remove all resources from the cluster"
	@echo "    make k8s-status         Show pod status in blockblast namespace"
	@echo ""
	@echo "  Other"
	@echo "    make clean              Remove build artefacts and caches"
	@echo ""

# ── Play ──────────────────────────────────────────────────────────────────────
play:
	@echo "Starting Block Blast..."
	docker compose up -d
	@echo ""
	@echo "  Game:    http://localhost:3000"
	@echo "  API:     http://localhost:8000"
	@echo ""
	@echo "Run 'make docker-logs' to tail logs, 'make docker-down' to stop."

# ── Install ───────────────────────────────────────────────────────────────────
install: install-backend install-frontend

install-backend:
	cd backend && uv sync

install-frontend:
	cd frontend && npm ci

# ── Development ───────────────────────────────────────────────────────────────
dev-backend:
	cd backend && uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	cd frontend && npm run dev

# ── Lint ──────────────────────────────────────────────────────────────────────
lint: lint-backend lint-frontend

lint-backend:
	cd backend && uv run ruff check

lint-frontend:
	cd frontend && npm run lint

# ── Format ────────────────────────────────────────────────────────────────────
format: format-backend format-frontend

format-backend:
	cd backend && uv run ruff format

format-frontend:
	cd frontend && npx prettier . --write

# ── Type check ────────────────────────────────────────────────────────────────
typecheck:
	cd backend && uv run pyrefly check

# ── Tests ─────────────────────────────────────────────────────────────────────
test: test-backend test-frontend

test-backend:
	cd backend && uv run pytest -m "not integration"

test-frontend:
	cd frontend && npm run test

test-integration:
	cd backend && uv run pytest -m "integration"

test-coverage:
	cd backend && uv run pytest --cov=src --cov-report=term-missing
	cd frontend && npm run test:coverage

# ── Docker ────────────────────────────────────────────────────────────────────
docker-build:
	docker compose build

docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f

# ── Kubernetes ────────────────────────────────────────────────────────────────
k8s-apply:
	kubectl apply -f k8s/

k8s-delete:
	kubectl delete -f k8s/

k8s-status:
	kubectl get pods -n blockblast

# ── Clean ─────────────────────────────────────────────────────────────────────
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .ruff_cache -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "coverage.xml" -delete
	rm -rf frontend/coverage
	rm -rf frontend/dist
