#!/bin/bash

set -e

# Se for primeira execução, inicializar projeto
if [ "$1" = "init" ]; then
    exec ./scripts/init-project.sh
fi

# Se for comando Django, rodar com manage.py
if [ "$1" = "manage" ]; then
    shift
    exec python manage.py "$@"
fi

# Caso contrário, executar comando normalmente
exec "$@"