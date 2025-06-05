.PHONY: help dev test build deploy clean logs backup version changelog release

# ==============================================================================
# VARIABLES & CONFIGURATION
# ==============================================================================

# Docker & Deployment Variables
DOCKER_REGISTRY ?= localhost:5000
APP_NAME = squadra-app
COMMIT_SHA = $(shell git rev-parse --short HEAD)
BRANCH = $(shell git branch --show-current)

# Remote VM Configuration
VM_HOST ?= 10.10.15.7  # IP da sua VM
VM_USER ?= your-user
DOCKER_CONTEXT_REMOTE = remote-vm

# Version & Build Variables
PYTHON := python
PIP := pip
MANAGE := $(PYTHON) manage.py
DATE := $(shell date +"%Y-%m-%d")
GIT_BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
GIT_COMMIT := $(shell git rev-parse --short HEAD)
CURRENT_VERSION := $(shell python -c "from apps.manager.version import __version__; print(__version__)" 2>/dev/null || echo "unknown")

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
PURPLE := \033[0;35m
CYAN := \033[0;36m
NC := \033[0m # No Color

# ==============================================================================
# HELP & INFO
# ==============================================================================

help: ## Show this help message
	@echo "$(BLUE)Chronos Project - Squad Projects Management$(NC)"
	@echo "============================================="
	@echo ""
	@echo "$(YELLOW)📱 Local Development (Mac):$(NC)"
	@echo "  dev                 Start development server locally"
	@echo "  test                Run tests locally"
	@echo "  migrate             Run migrations locally"
	@echo "  makemigrations      Create new migrations"
	@echo "  shell               Open Django shell"
	@echo "  init                Initialize project (first time setup)"
	@echo ""
	@echo "$(YELLOW)🔧 Version & Release Management:$(NC)"
	@echo "  version             Show current version information"
	@echo "  changelog           Generate automatic changelog"
	@echo "  changelog-detailed  Generate categorized changelog"
	@echo "  release             Prepare new release (bump version)"
	@echo "  tag                 Create Git tag (use: make tag VERSION=1.0.0)"
	@echo "  status              Show project status and metrics"
	@echo ""
	@echo "$(YELLOW)🐳 Remote Docker (VM):$(NC)"
	@echo "  setup-remote        Setup remote Docker context"
	@echo "  build-remote        Build Docker image on VM"
	@echo "  staging             Deploy to staging on VM"
	@echo "  production          Deploy to production on VM"
	@echo ""
	@echo "$(YELLOW)📊 Remote Management:$(NC)"
	@echo "  logs-staging        View staging logs (remote)"
	@echo "  logs-production     View production logs (remote)"
	@echo "  clean-remote        Clean Docker resources on VM"
	@echo "  status-remote       Show remote environment status"
	@echo ""
	@echo "$(YELLOW)🛠️  Utilities:$(NC)"
	@echo "  clean               Remove temporary files"
	@echo "  install             Install dependencies"
	@echo "  setup               Full project setup"
	@echo ""

# ==============================================================================
# VERSION & RELEASE MANAGEMENT
# ==============================================================================

version: ## Show current version information
	@echo "$(BLUE)📦 Chronos Version Information$(NC)"
	@echo "=================================="
	@python -c "from apps.manager.version import get_version_info; import json; info = get_version_info(); print(f'$(GREEN)Version:$(NC) {info[\"version\"]}'); print(f'$(GREEN)Codename:$(NC) {info[\"codename\"]}'); print(f'$(GREEN)Build Date:$(NC) {info[\"build_date\"]}'); print(f'$(GREEN)Git Branch:$(NC) {info[\"git\"][\"branch\"]}' if info['git']['branch'] else '$(GREEN)Git Branch:$(NC) N/A'); print(f'$(GREEN)Git Commit:$(NC) {info[\"git\"][\"commit_short\"]}' if info['git']['commit_short'] else '$(GREEN)Git Commit:$(NC) N/A'); print(f'$(GREEN)Is Dirty:$(NC) {\"Yes\" if info[\"git\"][\"is_dirty\"] else \"No\"}' if info['git']['commit_short'] else '')"

changelog: ## Generate automatic changelog (last 50 commits)
	@echo "$(BLUE)📝 Generating Automatic Changelog...$(NC)"
	@$(MAKE) changelog-auto

changelog-auto: ## Generate changelog based on Git commits
	@echo "# Changelog Automático - $(DATE)" > CHANGELOG_AUTO.md
	@echo "" >> CHANGELOG_AUTO.md
	@echo "Gerado automaticamente a partir do histórico do Git." >> CHANGELOG_AUTO.md
	@echo "" >> CHANGELOG_AUTO.md
	@echo "**Branch:** $(GIT_BRANCH) | **Commit:** $(GIT_COMMIT) | **Data:** $(DATE)" >> CHANGELOG_AUTO.md
	@echo "" >> CHANGELOG_AUTO.md
	@echo "---" >> CHANGELOG_AUTO.md
	@echo "" >> CHANGELOG_AUTO.md
	@git log --oneline --decorate --graph --max-count=50 --pretty=format:"- **%h** %s _%an, %ar_" >> CHANGELOG_AUTO.md
	@echo "" >> CHANGELOG_AUTO.md
	@echo "" >> CHANGELOG_AUTO.md
	@echo "---" >> CHANGELOG_AUTO.md
	@echo "" >> CHANGELOG_AUTO.md
	@echo "## Commits Detalhados" >> CHANGELOG_AUTO.md
	@echo "" >> CHANGELOG_AUTO.md
	@git log --max-count=20 --pretty=format:"### %s%n**Autor:** %an <%ae>%n**Data:** %ad%n**Commit:** %H%n%n%b%n---" --date=format:"%d/%m/%Y %H:%M" >> CHANGELOG_AUTO.md
	@echo "$(GREEN)✅ Changelog automático gerado em CHANGELOG_AUTO.md$(NC)"

changelog-detailed: ## Generate categorized changelog
	@echo "$(BLUE)📋 Generating Detailed Changelog...$(NC)"
	@echo "# Changelog Detalhado - $(DATE)" > CHANGELOG_DETAILED.md
	@echo "" >> CHANGELOG_DETAILED.md
	@echo "## 🆕 Novas Funcionalidades" >> CHANGELOG_DETAILED.md
	@git log --grep="feat\|add\|new" --oneline --pretty=format:"- %s (%h)" --since="1 month ago" >> CHANGELOG_DETAILED.md || echo "- Nenhuma nova funcionalidade encontrada" >> CHANGELOG_DETAILED.md
	@echo "" >> CHANGELOG_DETAILED.md
	@echo "" >> CHANGELOG_DETAILED.md
	@echo "## 🐛 Correções de Bugs" >> CHANGELOG_DETAILED.md
	@git log --grep="fix\|bug\|patch" --oneline --pretty=format:"- %s (%h)" --since="1 month ago" >> CHANGELOG_DETAILED.md || echo "- Nenhuma correção encontrada" >> CHANGELOG_DETAILED.md
	@echo "" >> CHANGELOG_DETAILED.md
	@echo "" >> CHANGELOG_DETAILED.md
	@echo "## 🔄 Melhorias" >> CHANGELOG_DETAILED.md
	@git log --grep="improve\|enhance\|update\|refactor" --oneline --pretty=format:"- %s (%h)" --since="1 month ago" >> CHANGELOG_DETAILED.md || echo "- Nenhuma melhoria encontrada" >> CHANGELOG_DETAILED.md
	@echo "" >> CHANGELOG_DETAILED.md
	@echo "" >> CHANGELOG_DETAILED.md
	@echo "## 📚 Documentação" >> CHANGELOG_DETAILED.md
	@git log --grep="doc\|readme\|comment" --oneline --pretty=format:"- %s (%h)" --since="1 month ago" >> CHANGELOG_DETAILED.md || echo "- Nenhuma atualização de documentação encontrada" >> CHANGELOG_DETAILED.md
	@echo "" >> CHANGELOG_DETAILED.md
	@echo "$(GREEN)✅ Changelog detalhado gerado em CHANGELOG_DETAILED.md$(NC)"

changelog-manual: ## Update main Changelog.md with template
	@echo "$(BLUE)📝 Updating Manual Changelog...$(NC)"
	@if [ ! -f "Changelog.md" ]; then \
		echo "# Changelog" > Changelog.md; \
		echo "" >> Changelog.md; \
		echo "Todas as mudanças notáveis neste projeto serão documentadas neste arquivo." >> Changelog.md; \
		echo "" >> Changelog.md; \
		echo "O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/)," >> Changelog.md; \
		echo "e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/)." >> Changelog.md; \
		echo "" >> Changelog.md; \
	fi
	@echo "" >> Changelog.md
	@echo "## [$(CURRENT_VERSION)] - $(DATE)" >> Changelog.md
	@echo "" >> Changelog.md
	@echo "### ✨ Adicionado" >> Changelog.md
	@echo "- " >> Changelog.md
	@echo "" >> Changelog.md
	@echo "### 🛠️ Alterado" >> Changelog.md
	@echo "- " >> Changelog.md
	@echo "" >> Changelog.md
	@echo "### 🔄 Melhorado" >> Changelog.md
	@echo "- " >> Changelog.md
	@echo "" >> Changelog.md
	@echo "### 🐛 Corrigido" >> Changelog.md
	@echo "- " >> Changelog.md
	@echo "" >> Changelog.md
	@echo "### 🗑️ Removido" >> Changelog.md
	@echo "- " >> Changelog.md
	@echo "" >> Changelog.md
	@echo "---" >> Changelog.md
	@echo "$(GREEN)✅ Template adicionado ao Changelog.md$(NC)"

release: ## Prepare new release (bump version and generate changelog)
	@echo "$(BLUE)🚀 Preparing New Release...$(NC)"
	@echo "Current version: $(PURPLE)$(CURRENT_VERSION)$(NC)"
	@read -p "$(YELLOW)New version (ex: 1.1.0): $(NC)" NEW_VERSION; \
	if [ -n "$$NEW_VERSION" ]; then \
		sed -i.bak "s/__version__ = \".*\"/__version__ = \"$$NEW_VERSION\"/" apps/manager/version.py; \
		sed -i.bak "s/__release_date__ = \".*\"/__release_date__ = \"$(DATE)\"/" apps/manager/version.py; \
		rm apps/manager/version.py.bak; \
		$(MAKE) changelog-auto; \
		$(MAKE) changelog-detailed; \
		echo "$(GREEN)✅ Version updated to $$NEW_VERSION$(NC)"; \
		echo "$(YELLOW)📝 Don't forget to update Changelog.md manually$(NC)"; \
		echo "$(YELLOW)🏷️  To create a tag: make tag VERSION=$$NEW_VERSION$(NC)"; \
	else \
		echo "$(RED)❌ Version not provided$(NC)"; \
	fi

tag: ## Create Git tag (use: make tag VERSION=1.0.0)
	@if [ -z "$(VERSION)" ]; then \
		echo "$(RED)❌ Use: make tag VERSION=1.0.0$(NC)"; \
		exit 1; \
	fi
	@echo "$(BLUE)🏷️  Creating tag v$(VERSION)...$(NC)"
	@git add -A
	@git commit -m "chore: release v$(VERSION)" || echo "Nothing to commit"
	@git tag -a "v$(VERSION)" -m "Release v$(VERSION) - Chronos Project"
	@echo "$(GREEN)✅ Tag v$(VERSION) created$(NC)"
	@echo "$(YELLOW)📤 To push: git push origin $(GIT_BRANCH) --tags$(NC)"

status: ## Show project status and metrics
	@echo "$(BLUE)📊 Chronos Project Status$(NC)"
	@echo "=========================="
	@echo "$(GREEN)📁 Directory:$(NC) $(PWD)"
	@echo "$(GREEN)🐍 Python:$(NC) $(shell python --version 2>/dev/null || echo 'Not available')"
	@echo "$(GREEN)🌿 Git Branch:$(NC) $(GIT_BRANCH)"
	@echo "$(GREEN)📝 Last Commit:$(NC) $(GIT_COMMIT)"
	@echo "$(GREEN)📦 Version:$(NC) $(CURRENT_VERSION)"
	@echo "$(GREEN)📊 Python Lines:$(NC) $(shell find . -name "*.py" -not -path "./venv/*" -not -path "./.venv/*" -not -path "./env/*" | xargs wc -l 2>/dev/null | tail -1 | awk '{print $$1}' || echo 'N/A')"
	@echo "$(GREEN)🗂️  Django Apps:$(NC) $(shell find ./apps -maxdepth 1 -type d -not -name "__pycache__" 2>/dev/null | wc -l | xargs echo || echo 'N/A')"
	@echo "$(GREEN)🐳 Docker Context:$(NC) $(shell docker context show 2>/dev/null || echo 'N/A')"

# ==============================================================================
# LOCAL DEVELOPMENT (Mac)
# ==============================================================================

dev: ## Start development server locally
	@echo "$(BLUE)🚀 Starting development server on Mac...$(NC)"
	@./scripts/run-local.sh uv run manage.py runserver

test: ## Run tests locally
	@echo "$(BLUE)🧪 Running tests on Mac...$(NC)"
	@./scripts/run-local.sh uv run manage.py test

migrate: ## Run migrations locally
	@echo "$(BLUE)📊 Running migrations on Mac...$(NC)"
	@./scripts/run-local.sh uv run manage.py migrate

makemigrations: ## Create migrations locally
	@echo "$(BLUE)📝 Creating migrations on Mac...$(NC)"
	@./scripts/run-local.sh uv run manage.py makemigrations

shell: ## Open Django shell locally
	@./scripts/run-local.sh uv run manage.py shell

collectstatic: ## Collect static files locally
	@./scripts/run-local.sh uv run manage.py collectstatic --noinput

init: ## Initialize project (first time setup)
	@echo "$(BLUE)🔧 Initializing project...$(NC)"
	@./scripts/run-local.sh ./scripts/init-project.sh

setup-superuser: ## Create superuser
	@echo "$(BLUE)👤 Setting up superuser...$(NC)"
	@./scripts/run-local.sh uv run manage.py setup_superuser --interactive

reset-db: ## Reset database and create superuser
	@echo "$(BLUE)🗑️  Resetting database...$(NC)"
	@rm -f db.sqlite3
	@./scripts/run-local.sh uv run manage.py migrate
	@./scripts/run-local.sh uv run manage.py setup_superuser

# ==============================================================================
# REMOTE SETUP
# ==============================================================================

setup-remote: ## Setup remote Docker context
	@echo "$(BLUE)🔧 Setting up remote Docker context...$(NC)"
	@docker context create $(DOCKER_CONTEXT_REMOTE) \
		--docker "host=ssh://$(VM_USER)@$(VM_HOST)" || \
		echo "Context already exists"
	@echo "$(GREEN)✅ Remote context configured$(NC)"
	@echo "Use 'docker context use $(DOCKER_CONTEXT_REMOTE)' to switch"

test-remote: ## Test remote connection
	@echo "$(BLUE)🔍 Testing remote Docker connection...$(NC)"
	@docker --context=$(DOCKER_CONTEXT_REMOTE) ps
	@echo "$(GREEN)✅ Remote connection working$(NC)"

# ==============================================================================
# REMOTE BUILD & DEPLOY
# ==============================================================================

build-remote: ## Build Docker image on VM with version info
	@echo "$(BLUE)🔨 Building Docker image on VM...$(NC)"
	@echo "$(CYAN)Branch:$(NC) $(BRANCH) | $(CYAN)Commit:$(NC) $(COMMIT_SHA) | $(CYAN)Version:$(NC) $(CURRENT_VERSION)"
	@rsync -av --exclude='.git' --exclude='__pycache__' --exclude='.env' \
		./ $(VM_USER)@$(VM_HOST):~/squad-projects/
	@docker --context=$(DOCKER_CONTEXT_REMOTE) build \
		--build-arg VERSION=$(CURRENT_VERSION) \
		--build-arg COMMIT_SHA=$(COMMIT_SHA) \
		--build-arg BUILD_DATE=$(DATE) \
		-t $(APP_NAME):$(COMMIT_SHA) \
		-t $(APP_NAME):$(CURRENT_VERSION) \
		-f ~/squad-projects/Dockerfile \
		~/squad-projects/
	@docker --context=$(DOCKER_CONTEXT_REMOTE) tag \
		$(APP_NAME):$(COMMIT_SHA) $(APP_NAME):latest
	@if [ "$(BRANCH)" = "main" ]; then \
		docker --context=$(DOCKER_CONTEXT_REMOTE) tag \
			$(APP_NAME):$(COMMIT_SHA) $(APP_NAME):stable; \
		echo "$(GREEN)✅ Tagged as stable (main branch)$(NC)"; \
	fi

staging: build-remote ## Deploy to staging on VM
	@echo "$(BLUE)🚀 Deploying to staging on VM...$(NC)"
	@if [ "$(BRANCH)" != "staging" ] && [ "$(BRANCH)" != "develop" ]; then \
		echo "$(RED)❌ Staging can only be deployed from 'staging' or 'develop' branch$(NC)"; \
		echo "Current branch: $(YELLOW)$(BRANCH)$(NC)"; \
		exit 1; \
	fi
	@ssh $(VM_USER)@$(VM_HOST) "cd ~/squad-projects && \
		export TAG=$(COMMIT_SHA) && \
		export VERSION=$(CURRENT_VERSION) && \
		docker-compose -f infra/docker/compose/staging.yml up -d --build"
	@echo "$(GREEN)✅ Staging deployed$(NC)"
	@echo "$(CYAN)Version:$(NC) $(CURRENT_VERSION) | $(CYAN)Tag:$(NC) $(COMMIT_SHA)"
	@echo "$(CYAN)🌐 Access:$(NC) http://$(VM_HOST):8080"

production: build-remote ## Deploy to production on VM
	@echo "$(BLUE)🚀 Deploying to production on VM...$(NC)"
	@if [ "$(BRANCH)" != "main" ]; then \
		echo "$(RED)❌ Production can only be deployed from 'main' branch$(NC)"; \
		echo "Current branch: $(YELLOW)$(BRANCH)$(NC)"; \
		exit 1; \
	fi
	@echo "$(RED)⚠️  You are about to deploy to PRODUCTION on VM!$(NC)"
	@echo "$(CYAN)Branch:$(NC) $(BRANCH) | $(CYAN)Version:$(NC) $(CURRENT_VERSION) | $(CYAN)Commit:$(NC) $(COMMIT_SHA)"
	@read -p "Continue? [y/N] " confirm && [ "$$confirm" = "y" ]
	@ssh $(VM_USER)@$(VM_HOST) "cd ~/squad-projects && \
		export TAG=$(COMMIT_SHA) && \
		export VERSION=$(CURRENT_VERSION) && \
		docker-compose -f infra/docker/compose/production.yml up -d --build"
	@echo "$(GREEN)✅ Production deployed$(NC)"
	@echo "$(CYAN)Version:$(NC) $(CURRENT_VERSION) | $(CYAN)Tag:$(NC) $(COMMIT_SHA)"
	@echo "$(CYAN)🌐 Access:$(NC) https://app.squadra.dev.br"

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
	@echo "$(RED)⚠️  Opening shell in PRODUCTION on VM!$(NC)"
	@read -p "Continue? [y/N] " confirm && [ "$$confirm" = "y" ]
	@docker --context=$(DOCKER_CONTEXT_REMOTE) \
		compose -f infra/docker/compose/production.yml exec web python manage.py shell

staging-migrate: ## Run migrations in staging on VM
	@echo "$(BLUE)📊 Running migrations in staging on VM...$(NC)"
	@docker --context=$(DOCKER_CONTEXT_REMOTE) \
		compose -f infra/docker/compose/staging.yml exec web python manage.py migrate

production-migrate: ## Run migrations in production on VM
	@echo "$(BLUE)📊 Running migrations in production on VM...$(NC)"
	@echo "$(RED)⚠️  You are about to run migrations in PRODUCTION on VM!$(NC)"
	@read -p "Continue? [y/N] " confirm && [ "$$confirm" = "y" ]
	@docker --context=$(DOCKER_CONTEXT_REMOTE) \
		compose -f infra/docker/compose/production.yml exec web python manage.py migrate

# ==============================================================================
# REMOTE UTILITIES
# ==============================================================================

status-remote: ## Show remote environment status with version info
	@echo "$(BLUE)📊 Remote Environment Status ($(VM_HOST))$(NC)"
	@echo "========================================="
	@echo "$(GREEN)Current branch:$(NC) $(BRANCH)"
	@echo "$(GREEN)Current commit:$(NC) $(COMMIT_SHA)"
	@echo "$(GREEN)Local version:$(NC) $(CURRENT_VERSION)"
	@echo ""
	@echo "$(YELLOW)Docker images on VM:$(NC)"
	@docker --context=$(DOCKER_CONTEXT_REMOTE) images $(APP_NAME) \
		--format "table {{.Repository}}\t{{.Tag}}\t{{.CreatedAt}}\t{{.Size}}"
	@echo ""
	@echo "$(YELLOW)Running containers on VM:$(NC)"
	@docker --context=$(DOCKER_CONTEXT_REMOTE) ps \
		--format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

clean-remote: ## Clean Docker resources on VM
	@echo "$(BLUE)🧹 Cleaning Docker resources on VM...$(NC)"
	@docker --context=$(DOCKER_CONTEXT_REMOTE) \
		compose -f infra/docker/compose/staging.yml down -v
	@docker --context=$(DOCKER_CONTEXT_REMOTE) system prune -f
	@echo "$(GREEN)✅ Remote cleanup completed$(NC)"

backup-staging-remote: ## Backup staging database on VM
	@echo "$(BLUE)📦 Creating staging backup on VM...$(NC)"
	@ssh $(VM_USER)@$(VM_HOST) "mkdir -p ~/backups/staging"
	@docker --context=$(DOCKER_CONTEXT_REMOTE) \
		compose -f infra/docker/compose/staging.yml exec -T db \
		pg_dump -U staging_user staging_db > \
		~/backups/staging/staging_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)✅ Staging backup completed on VM$(NC)"

# ==============================================================================
# SYNC & UTILITIES
# ==============================================================================

sync: ## Sync code to VM
	@echo "$(BLUE)📤 Syncing code to VM...$(NC)"
	@rsync -av --exclude='.git' --exclude='__pycache__' --exclude='.env' \
		--exclude='node_modules' --exclude='venv' \
		./ $(VM_USER)@$(VM_HOST):~/squad-projects/
	@echo "$(GREEN)✅ Code synced to VM$(NC)"

deploy-code: sync build-remote ## Sync code and build

switch-remote: ## Switch to remote Docker context
	@docker context use $(DOCKER_CONTEXT_REMOTE)
	@echo "$(GREEN)✅ Switched to remote Docker context$(NC)"

switch-local: ## Switch to local Docker context
	@docker context use default
	@echo "$(GREEN)✅ Switched to local Docker context$(NC)"

# ==============================================================================
# UTILITIES & MAINTENANCE
# ==============================================================================

clean: ## Remove temporary files
	@echo "$(BLUE)🧹 Cleaning temporary files...$(NC)"
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type f -name "*.log" -delete
	@find . -type f -name ".DS_Store" -delete
	@rm -f CHANGELOG_AUTO.md CHANGELOG_DETAILED.md
	@echo "$(GREEN)✅ Cleanup completed$(NC)"

install: ## Install dependencies
	@echo "$(BLUE)🔧 Installing dependencies...$(NC)"
	@$(PIP) install -r requirements.txt
	@echo "$(GREEN)✅ Dependencies installed$(NC)"

setup: ## Full project setup
	@echo "$(BLUE)🔧 Full Chronos setup...$(NC)"
	@$(MAKE) install
	@$(MAKE) migrate
	@$(MAKE) collectstatic
	@echo "$(GREEN)✅ Setup completed$(NC)"
	@echo "$(YELLOW)📝 Run 'make setup-superuser' to create an admin user$(NC)"

# ==============================================================================
# REMOTE INITIALIZATION
# ==============================================================================

init-staging: ## Initialize staging environment
	@echo "$(BLUE)🔧 Initializing staging environment...$(NC)"
	@ssh $(VM_USER)@$(VM_HOST) "cd ~/squad-projects && \
		export DJANGO_ENVIRONMENT=staging && \
		docker-compose -f infra/docker/compose/staging.yml exec web \
		./scripts/init-project.sh"

init-production: ## Initialize production environment
	@echo "$(BLUE)🔧 Initializing production environment...$(NC)"
	@echo "$(RED)⚠️  You are about to initialize PRODUCTION!$(NC)"
	@read -p "Continue? [y/N] " confirm && [ "$$confirm" = "y" ]
	@ssh $(VM_USER)@$(VM_HOST) "cd ~/squad-projects && \
		export DJANGO_ENVIRONMENT=production && \
		docker-compose -f infra/docker/compose/production.yml exec web \
		./scripts/init-project.sh"
