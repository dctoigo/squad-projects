
# 🚀 Gestão de Projetos Autônomos

Sistema de gestão de projetos, tarefas e controle de tempo para profissionais autônomos e pequenas equipes.

---

## 🎯 Objetivo

Automatizar e centralizar o controle de:

- Projetos
- Tarefas
- Sessões de tempo (Time Tracking)
- Faturamento e relatórios
- Controle financeiro integrado
- Acesso remoto seguro (Cloudflare Tunnel)

---

## 📚 Documentação

- [Guia de Configuração do Ambiente (SETUP.md)](./SETUP.md)

---

## 🧰 Tecnologias utilizadas

- 🐍 **Python 3.10+**
- 🌐 **Django 4.x**
- 🐳 **Docker** + **Docker Compose**
- 🐘 **PostgreSQL** (local ou [Neon.tech](https://neon.tech))
- ⚙️ **Gunicorn** + **NGINX**
- ☁️ **Cloudflare Tunnel** (Argo Tunnel)
- 🚀 **GitHub Actions** (CI/CD)
- 🖥️ **Portainer** (opcional, para gerenciamento de stacks)

---

## ⚙️ Como rodar localmente

1️⃣ Clone o projeto:

```bash
git clone git@github.com:seu_usuario/gestao-projetos.git
cd gestao-projetos
```

2️⃣ Siga o [SETUP.md](./SETUP.md) para configurar o ambiente local.

3️⃣ Suba a aplicação:

```bash
docker-compose up -d --build
```

4️⃣ Migre o banco:

```bash
docker-compose exec web python manage.py migrate
```

5️⃣ Coletar estáticos:

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

6️⃣ Acesse em:

```
http://localhost
```

---

## 🌐 Acesso remoto (produção ou staging)

Configurar Cloudflare Tunnel:

```bash
docker-compose -f docker-compose.cloudflared.yml up -d
```

Acesso pelo domínio configurado (exemplo):

```
https://app.seudominio.com
```

---

## ✅ CI/CD

O projeto inclui exemplo de **workflow GitHub Actions** para:

- Rodar migrações
- Rodar testes
- Deploy automático (futuro)

---

## 🛡️ Segurança recomendada

- Usar **Cloudflare Access** para proteger o painel administrativo
- Usar HTTPS completo
- Restringir IPs e permissões conforme o ambiente

---

## 📄 Licença

Projeto privado - uso autorizado apenas para < SEU NOME / SUA EMPRESA >.

---

**© Gestão de Projetos Autônomos — 2025** 🚀

---
