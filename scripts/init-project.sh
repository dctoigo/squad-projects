#!/bin/bash

set -e

echo "🚀 Initializing Squad Projects..."

# Verificar se as variáveis de ambiente estão definidas
if [ -z "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "❌ DJANGO_SUPERUSER_PASSWORD environment variable is required"
    exit 1
fi

# Aguardar banco de dados (se usando Docker)
echo "⏳ Waiting for database..."
python manage.py wait_for_db 2>/dev/null || sleep 5

# Executar migrações
echo "📊 Running migrations..."
python manage.py migrate

# Coletar arquivos estáticos
echo "📂 Collecting static files..."
python manage.py collectstatic --noinput

# Criar superuser se não existir
echo "👤 Setting up superuser..."
python manage.py setup_superuser

echo "✅ Project initialized successfully!"
echo "🌐 Admin panel: http://localhost:8000/admin/"
echo "👤 Username: ${DJANGO_SUPERUSER_USERNAME:-admin}"