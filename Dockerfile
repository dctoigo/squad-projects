
# Base image
FROM python:3.10-slim

# Desabilita cache do Python
ENV PYTHONUNBUFFERED 1

# Define diretório de trabalho
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    netcat \
    && apt-get clean

# Copia requirements.txt e instala dependências Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . /app/

# Garante que diretórios de static/media existam
RUN mkdir -p /app/static /app/media

# Comando padrão: iniciar Gunicorn
CMD ["gunicorn", "gestao_projetos.wsgi:application", "--bind", "0.0.0.0:8000"]
