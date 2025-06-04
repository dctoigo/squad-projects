.PHONY: help dev test build deploy clean logs backup

# Variables
DOCKER_REGISTRY ?= localhost:5000
APP_NAME = squadra-app
COMMIT_SHA = $(shell git rev-parse --short HEAD)
BRANCH = $(shell git branch --show-current)

# Remote VM Configuration
VM_HOST ?= 10.10.15.7  # IP da sua VM
VM_USER ?= your-user
DOCKER_CONTEXT_REMOTE = remote-vm

# Help
help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Development (Local Mac):"
	@echo "  dev                 Start development server locally"
	@echo "  test                Run tests locally"
	@echo "  migrate             Run migrations locally"
	@echo "  makemigrations      Create new migrations"
	@echo "  shell               Open Django shell"
	@echo ""
	@echo "Remote Docker (VM):"
	@echo "  setup-remote        Setup remote Docker context"
	@echo "  build-remote        Build Docker image on VM"
	@echo "  staging             Deploy to staging on VM"
	@echo "  production          Deploy to production on VM"
	@echo ""
	@echo "Management:"
	@echo "  logs-staging        View staging logs (remote)"
	@echo "  logs-production     View production logs (remote)"
	@echo "  clean-remote        Clean Docker resources on VM"
	@echo "  status-remote       Show remote environment status"

# ==============================================================================
# LOCAL DEVELOPMENT (Mac)
# ==============================================================================

dev: ## Start development server locally
	@echo "🚀 Starting development server on Mac..."
	@./scripts/run-local.sh uv run manage.py runserver

test: ## Run tests locally
	@echo "🧪 Running tests on Mac..."
	@./scripts/run-local.sh uv run manage.py test

migrate: ## Run migrations locally
	@echo "📊 Running migrations on Mac..."
	@./scripts/run-local.sh uv run manage.py migrate

makemigrations: ## Create migrations locally
	@echo "📝 Creating migrations on Mac..."
	@./scripts/run-local.sh uv run manage.py makemigrations

shell: ## Open Django shell locally
	@./scripts/run-local.sh uv run manage.py shell

collectstatic: ## Collect static files locally
	@./scripts/run-local.sh uv run manage.py collectstatic --noinput

init: ## Initialize project (first time setup)
	@echo "🔧 Initializing project..."
	@./scripts/run-local.sh ./scripts/init-project.sh

setup-superuser: ## Create superuser
	@echo "👤 Setting up superuser..."
	@./scripts/run-local.sh uv run manage.py setup_superuser --interactive

reset-db: ## Reset database and create superuser
	@echo "🗑️  Resetting database..."
	@rm -f db.sqlite3
	@./scripts/run-local.sh uv run manage.py migrate
	@./scripts/run-local.sh uv run manage.py setup_superuser

# ==============================================================================
# REMOTE SETUP
# ==============================================================================

setup-remote: ## Setup remote Docker context
	@echo "🔧 Setting up remote Docker context..."
	@docker context create $(DOCKER_CONTEXT_REMOTE) \
		--docker "host=ssh://$(VM_USER)@$(VM_HOST)" || \
		echo "Context already exists"
	@echo "✅ Remote context configured"
	@echo "Use 'docker context use $(DOCKER_CONTEXT_REMOTE)' to switch"

test-remote: ## Test remote connection
	@echo "🔍 Testing remote Docker connection..."
	@docker --context=$(DOCKER_CONTEXT_REMOTE) ps
	@echo "✅ Remote connection working"

# ==============================================================================
# REMOTE BUILD & DEPLOY
# ==============================================================================

build-remote: ## Build Docker image on VM
	@echo "🔨 Building Docker image on VM..."
	@echo "Branch: $(BRANCH) | Commit: $(COMMIT_SHA)"
	@rsync -av --exclude='.git' --exclude='__pycache__' --exclude='.env' \
		./ $(VM_USER)@$(VM_HOST):~/squad-projects/
	@docker --context=$(DOCKER_CONTEXT_REMOTE) build \
		-t $(APP_NAME):$(COMMIT_SHA) \
		-f ~/squad-projects/Dockerfile \
		~/squad-projects/
	@docker --context=$(DOCKER_CONTEXT_REMOTE) tag \
		$(APP_NAME):$(COMMIT_SHA) $(APP_NAME):latest
	@if [ "$(BRANCH)" = "main" ]; then \
		docker --context=$(DOCKER_CONTEXT_REMOTE) tag \
			$(APP_NAME):$(COMMIT_SHA) $(APP_NAME):stable; \
		echo "✅ Tagged as stable (main branch)"; \
	fi

staging: build-remote ## Deploy to staging on VM
	@echo "🚀 Deploying to staging on VM..."
	@if [ "$(BRANCH)" != "staging" ] && [ "$(BRANCH)" != "develop" ]; then \
		echo "❌ Staging can only be deployed from 'staging' or 'develop' branch"; \
		echo "Current branch: $(BRANCH)"; \
		exit 1; \
	fi
	@ssh $(VM_USER)@$(VM_HOST) "cd ~/squad-projects && \
		export TAG=$(COMMIT_SHA) && \
		docker-compose -f infra/docker/compose/staging.yml up -d --build"
	@echo "✅ Staging deployed with tag: $(COMMIT_SHA)"
	@echo "🌐 Access: http://$(VM_HOST):8080"

production: build-remote ## Deploy to production on VM
	@echo "🚀 Deploying to production on VM..."
	@if [ "$(BRANCH)" != "main" ]; then \
		echo "❌ Production can only be deployed from 'main' branch"; \
		echo "Current branch: $(BRANCH)"; \
		exit 1; \
	fi
	@echo "⚠️  You are about to deploy to PRODUCTION on VM!"
	@echo "Branch: $(BRANCH) | Commit: $(COMMIT_SHA)"
	@read -p "Continue? [y/N] " confirm && [ "$$confirm" = "y" ]
	@ssh $(VM_USER)@$(VM_HOST) "cd ~/squad-projects && \
		export TAG=$(COMMIT_SHA) && \
		docker-compose -f infra/docker/compose/production.yml up -d --build"
	@echo "✅ Production deployed with tag: $(COMMIT_SHA)"
	@echo "🌐 Access: https://app.squadra.dev.br"

# ==============================================================================
# REMOTE MANAGEMENT
# ==============================================================================

staging-logs: ## View staging logs on VM
	@docker --context=$(DOCKER_CONTEXT_REMOTE) \
		compose -f infra/docker/compose/staging.yml logs -f web

production-logs: ## View production logs on VM
	@docker --context=$(DOCKER_CONTEXT_REMOTE) \
		compose -f infra/docker/compose/production.yml logs -f web

staging-shell: ## Open shell in staging on VM
	@docker --context=$(DOCKER_CONTEXT_REMOTE) \
		compose -f infra/docker/compose/staging.yml exec web python manage.py shell

production-shell: ## Open shell in production on VM
	@echo "⚠️  Opening shell in PRODUCTION on VM!"
	@read -p "Continue? [y/N] " confirm && [ "$$confirm" = "y" ]
	@docker --context=$(DOCKER_CONTEXT_REMOTE) \
		compose -f infra/docker/compose/production.yml exec web python manage.py shell

staging-migrate: ## Run migrations in staging on VM
	@echo "📊 Running migrations in staging on VM..."
	@docker --context=$(DOCKER_CONTEXT_REMOTE) \
		compose -f infra/docker/compose/staging.yml exec web python manage.py migrate

production-migrate: ## Run migrations in production on VM
	@echo "📊 Running migrations in production on VM..."
	@echo "⚠️  You are about to run migrations in PRODUCTION on VM!"
	@read -p "Continue? [y/N] " confirm && [ "$$confirm" = "y" ]
	@docker --context=$(DOCKER_CONTEXT_REMOTE) \
		compose -f infra/docker/compose/production.yml exec web python manage.py migrate

# ==============================================================================
# REMOTE UTILITIES
# ==============================================================================

status-remote: ## Show remote environment status
	@echo "📊 Remote Environment Status ($(VM_HOST))"
	@echo "========================================="
	@echo "Current branch: $(BRANCH)"
	@echo "Current commit: $(COMMIT_SHA)"
	@echo ""
	@echo "Docker images on VM:"
	@docker --context=$(DOCKER_CONTEXT_REMOTE) images $(APP_NAME) \
		--format "table {{.Repository}}\t{{.Tag}}\t{{.CreatedAt}}\t{{.Size}}"
	@echo ""
	@echo "Running containers on VM:"
	@docker --context=$(DOCKER_CONTEXT_REMOTE) ps \
		--format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

clean-remote: ## Clean Docker resources on VM
	@echo "🧹 Cleaning Docker resources on VM..."
	@docker --context=$(DOCKER_CONTEXT_REMOTE) \
		compose -f infra/docker/compose/staging.yml down -v
	@docker --context=$(DOCKER_CONTEXT_REMOTE) system prune -f
	@echo "✅ Remote cleanup completed"

backup-staging-remote: ## Backup staging database on VM
	@echo "📦 Creating staging backup on VM..."
	@ssh $(VM_USER)@$(VM_HOST) "mkdir -p ~/backups/staging"
	@docker --context=$(DOCKER_CONTEXT_REMOTE) \
		compose -f infra/docker/compose/staging.yml exec -T db \
		pg_dump -U staging_user staging_db > \
		~/backups/staging/staging_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ Staging backup completed on VM"

# ==============================================================================
# SYNC & UTILITIES
# ==============================================================================

sync: ## Sync code to VM
	@echo "📤 Syncing code to VM..."
	@rsync -av --exclude='.git' --exclude='__pycache__' --exclude='.env' \
		--exclude='node_modules' --exclude='venv' \
		./ $(VM_USER)@$(VM_HOST):~/squad-projects/
	@echo "✅ Code synced to VM"

deploy-code: sync build-remote ## Sync code and build

switch-remote: ## Switch to remote Docker context
	@docker context use $(DOCKER_CONTEXT_REMOTE)
	@echo "✅ Switched to remote Docker context"

switch-local: ## Switch to local Docker context
	@docker context use default
	@echo "✅ Switched to local Docker context"

# ==============================================================================
# REMOTE INITIALIZATION
# ==============================================================================

init-staging: ## Initialize staging environment
	@echo "🔧 Initializing staging environment..."
	@ssh $(VM_USER)@$(VM_HOST) "cd ~/squad-projects && \
		export DJANGO_ENVIRONMENT=staging && \
		docker-compose -f infra/docker/compose/staging.yml exec web \
		./scripts/init-project.sh"

init-production: ## Initialize production environment
	@echo "🔧 Initializing production environment..."
	@echo "⚠️  You are about to initialize PRODUCTION!"
	@read -p "Continue? [y/N] " confirm && [ "$$confirm" = "y" ]
	@ssh $(VM_USER)@$(VM_HOST) "cd ~/squad-projects && \
		export DJANGO_ENVIRONMENT=production && \
		docker-compose -f infra/docker/compose/production.yml exec web \
		./scripts/init-project.sh"
