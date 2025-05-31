
# Gestão de Projetos Autônomos  
## 🛠️ Guia de Configuração do Ambiente Local (SETUP.md)

---

## 🎯 Objetivo

Este guia descreve como configurar o ambiente de desenvolvimento e produção local para o sistema **Gestão de Projetos Autônomos**, utilizando:

- Docker (Docker Compose)
- PostgreSQL (local ou Neon Cloud)
- Django com Gunicorn e NGINX
- Cloudflare Tunnel para acesso remoto seguro com seu domínio

---

## 📦 Requisitos

### 1️⃣ Softwares necessários:

- [Docker](https://www.docker.com/products/docker-desktop) (>= 24.x)
- [Docker Compose](https://docs.docker.com/compose/) (>= 2.x)
- Conta no [Cloudflare](https://cloudflare.com) (gratuita)
- Domínio próprio gerenciado pelo Cloudflare
- Conta no [Neon.tech](https://neon.tech) (opcional, banco em nuvem)

---

## ⚙️ Estrutura de Diretórios

```plaintext
gestao-projetos/
├── apps/
├── config/
│   └── nginx/
│       └── gestao.conf
├── cloudflared/
│   └── config.yml
├── static/
├── media/
├── .env
├── docker-compose.yml
├── docker-compose.cloudflared.yml
├── Dockerfile
├── requirements.txt
├── manage.py
└── gestao_projetos/
    ├── settings/
    │   ├── __init__.py
    │   ├── base.py
    │   ├── dev.py
    │   ├── staging.py
    │   └── prod.py
```

---

## 🚀 Passo a Passo de Configuração

---

### ✅ 1️⃣ Clonar o repositório

```bash
git clone git@github.com:seu_usuario/gestao-projetos.git
cd gestao-projetos
```

---

### ✅ 2️⃣ Configurar variáveis de ambiente

Crie o arquivo `.env` na raiz do projeto:

```env
# Comum
SECRET_KEY=seu-segredo
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 app.seudominio.com

# URLs Neon ou local
NEON_DEV_URL=postgres://usuario:senha@dev.dbname.neon.tech/dbname
NEON_STAGING_URL=postgres://usuario:senha@staging.dbname.neon.tech/dbname
NEON_PROD_URL=postgres://usuario:senha@main.dbname.neon.tech/dbname
```

**Obs:** Se estiver rodando PostgreSQL local, você pode configurar:

```env
DATABASE_URL=postgres://usuario:senha@db:5432/gestao
```

---

### ✅ 3️⃣ Build da aplicação

```bash
docker-compose up -d --build
```

---

### ✅ 4️⃣ Migrar banco e coletar estáticos

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
```

---

### ✅ 5️⃣ Acessar localmente

- Local: [http://localhost](http://localhost)

---

## 🌐 Acesso Remoto com Cloudflare Tunnel

---

### ✅ 1️⃣ Instalar Cloudflared

```bash
docker pull cloudflare/cloudflared:latest
```

---

### ✅ 2️⃣ Criar túnel no Cloudflare

```bash
cloudflared tunnel login
cloudflared tunnel create gestao-projetos-tunnel
```

---

### ✅ 3️⃣ Configurar `cloudflared/config.yml`

```yaml
tunnel: meu-tunel-id
credentials-file: /etc/cloudflared/<tunnel-id>.json

ingress:
  - hostname: app.seudominio.com
    service: http://nginx:80
  - service: http_status:404
```

---

### ✅ 4️⃣ Docker Compose para Cloudflared

`docker-compose.cloudflared.yml`

```yaml
services:
  cloudflared:
    image: cloudflare/cloudflared:latest
    restart: unless-stopped
    command: tunnel --config /etc/cloudflared/config.yml run
    volumes:
      - ./cloudflared:/etc/cloudflared
```

---

### ✅ 5️⃣ Subir o túnel

```bash
docker-compose -f docker-compose.cloudflared.yml up -d
```

---

## ✅ Comandos úteis

| Ação | Comando |
|------|---------|
| Subir aplicação | `docker-compose up -d --build` |
| Subir túnel | `docker-compose -f docker-compose.cloudflared.yml up -d` |
| Migrar banco | `docker-compose exec web python manage.py migrate` |
| Coletar estáticos | `docker-compose exec web python manage.py collectstatic --noinput` |
| Acessar shell | `docker-compose exec web python manage.py shell` |

---

## ⚙️ Uso com Docker Compose ou Portainer

### ➜ Usando diretamente com **Docker Compose** (recomendado para desenvolvimento/testes):

```bash
# Subir aplicação
docker-compose up -d --build

# Subir túnel
docker-compose -f docker-compose.cloudflared.yml up -d
```

Você pode manter um **arquivo .env** separado para cada ambiente e alternar com `DJANGO_ENV=dev`, `DJANGO_ENV=staging`, etc.

### ➜ Usando com **Portainer**:

1. Adicione a stack pelo painel Portainer usando:
    - `docker-compose.yml` (para app)
    - `docker-compose.cloudflared.yml` (para túnel)

2. No Portainer:
    - Crie a stack e aponte para o seu repositório Git (recomendado), ou
    - Copie o conteúdo dos `docker-compose` e cole na stack.

3. Variáveis de ambiente:
    - No Portainer, você pode definir as variáveis `.env` diretamente na stack ou manter o arquivo `.env` no diretório do projeto.

4. Gerenciamento:
    - Portainer facilita subir/descer containers, escalar, visualizar logs, etc.

---

## 🛠️ Ambientes suportados

| Ambiente | Django ENV | Banco de Dados |
|----------|------------|----------------|
| Desenvolvimento | `dev` | `NEON_DEV_URL` ou local |
| Staging | `staging` | `NEON_STAGING_URL` |
| Produção | `prod` | `NEON_PROD_URL` |

Use a variável:

```bash
export DJANGO_ENV=dev
```

---

## 📝 Notas finais

- Neon: banco **branch-based**, ideal para ambientes isolados.
- Cloudflare Tunnel: acesso **seguro**, sem abrir portas na firewall.
- Integração com **GitHub Actions** para CI/CD automatizado (exemplo de workflow recomendado).
- Pode ser integrado a stacks gerenciadas via **Portainer** sem problemas.

---

**© Gestão de Projetos Autônomos — Setup Guide** 🚀
