# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## Como Usar

### 📋 Manual
Edite este arquivo manualmente para documentar mudanças importantes.

### 🤖 Automático
```bash
# 1. Verificar status atual
make status

# 2. Gerar changelog
make changelog

# 3. Preparar nova release
make release

# 4. Criar tag
make tag VERSION=1.1.0

# 5. Deploy para staging
make staging

# 6. Deploy para produção (se main branch)
make production
```

---

## [Unreleased]

### ✨ Added
- Sistema de versionamento automático com `version.py`
- Makefile para automação de changelog e releases
- Integração Git para informações de build
- Context processor para versão no template

### 🛠️ Changed
- Footer atualizado com informações de versão dinâmicas
- Estrutura preparada para releases automatizadas

### 🔄 Improved
- Processo de release mais profissional
- Rastreabilidade de versões melhorada

---

### ✨ Added
- Chronos visual identity: new logo, favicon, color palette and styling adjustments
- Updated About page with Chronos brand
- Prepared for N8N / API integration (initial structuring)

### 🛠️ Changed
- Project settings refactored to support multiple environments:
  - `settings/base.py`, `settings/dev.py`, `settings/prod.py`
  - `.envs/` directory
  - Docker Compose files per environment
- Navbar updated with new styling and branding

### 🔄 Improved
- Project structure more maintainable and ready for scaling
- Better environment isolation for development and production

---

This release marks the **rebranding of the application to "Chronos"** and a technical milestone towards a modular, API-first architecture.