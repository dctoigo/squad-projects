#!/bin/bash

# Carregar variáveis do .env.development
if [ -f .env.development ]; then
    export $(grep -v '^#' .env.development | xargs)
fi

# Definir ambiente
export DJANGO_ENVIRONMENT=development

# Executar comando passado como parâmetro
exec "$@"