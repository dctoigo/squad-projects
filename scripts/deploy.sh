#!/bin/bash

ENVIRONMENT=$1
TAG=${2:-latest}

case $ENVIRONMENT in
  "staging")
    echo "Deploying to staging..."
    docker-compose -f docker-compose.staging.yml up -d --build
    ;;
  "production")
    echo "Deploying to production..."
    docker-compose -f docker-compose.production.yml up -d --build
    ;;
  *)
    echo "Usage: ./deploy.sh [staging|production] [tag]"
    exit 1
    ;;
esac