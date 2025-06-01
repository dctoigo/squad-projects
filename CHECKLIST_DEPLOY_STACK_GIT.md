
# ✅ CHECKLIST_DEPLOY_STACK_GIT.md — Deploy de Stack via Git no Portainer

Este checklist explica o fluxo recomendado para deploy da stack `squad-projects` utilizando o recurso **Deploy from Git** do Portainer.

---

## 🚀 Objetivo

Garantir que:

✅ Todo o código da stack venha do repositório Git (ex: GitHub).  
✅ Não seja necessário clonar o repositório ou criar diretórios manualmente na VM.  
✅ O Portainer gerencie a stack de forma consistente e rastreável (GitOps).

---

## 🚀 Fluxo recomendado (GitOps)

### 1️⃣ Commit e Push

✅ Realize o desenvolvimento local.  
✅ Teste localmente (opcional).  
✅ Faça **commit** e **push** para o repositório Git (ex: GitHub).

Exemplo:

```bash
git add .
git commit -m "Ajustes na stack / NGINX / configs"
git push origin main
```

---

### 2️⃣ Deploy no Portainer

✅ Acesse Portainer → Stacks → **Add Stack** → Git Repository.

Campos:

| Campo | Valor |
|-------|-------|
| Repository URL | `https://github.com/squadra/squad-projects.git` |
| Compose path | `docker-compose.yml` |

Opções:

✅ **Re-pull image**  
✅ **Rebuild**  
✅ **Recreate volumes** (se aplicável)

**Deploy the Stack**.

---

### 3️⃣ O que o Portainer faz

✅ Clona automaticamente o repositório (ex: em `/data/compose/...`).  
✅ Usa o `docker-compose.yml` do repositório.  
✅ Cria os diretórios automaticamente com base no repositório: **não é necessário clonar ou criar manualmente**.  
✅ Monta volumes relativos (ex: `./config/nginx → /etc/nginx/conf.d`) com base no clone do repositório.

---

## 🚀 Atualizando a stack

Após um novo push para o Git:

1️⃣ Acesse a Stack no Portainer.  
2️⃣ Clique em:

```plaintext
Pull latest commit
```

3️⃣ Opcional: clique em **Re-deploy** com:

✅ Re-pull  
✅ Rebuild

---

## 🚀 Quando NÃO usar clone manual

✅ Não é necessário clonar o repositório manualmente na VM.  
✅ Não é necessário criar diretórios manualmente.  
✅ Não é necessário executar `docker-compose` manualmente (exceto para debug local).

O Portainer gerencia tudo automaticamente.

---

## 🚀 Debug local (opcional)

Se desejar rodar localmente:

```bash
git clone https://github.com/squadra/squad-projects.git
cd squad-projects
docker-compose up -d --build
```

---

# 🚀 Conclusão

✅ Usando **Deploy from Git** + GitOps:

✅ Stack sempre consistente com o repositório.  
✅ Controle total de versões.  
✅ Zero necessidade de manutenção manual de diretórios na VM.  
✅ Portainer gerencia o ciclo de vida da stack.

---

**© Squad Projects — Deploy Stack via Git Checklist 🚀**
