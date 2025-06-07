#!/bin/bash

# Full paths to Docker binaries
DOCKER="/Applications/Docker.app/Contents/Resources/bin/docker"
DOCKER_COMPOSE="/Applications/Docker.app/Contents/Resources/bin/docker-compose"

# Stop any existing containers
$DOCKER stop family_finance_db || true
$DOCKER rm family_finance_db || true

# Start PostgreSQL container
$DOCKER run --name family_finance_db \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=family_finance \
    -p 5432:5432 \
    -d postgres:14

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
sleep 5

# Test the connection
$DOCKER exec family_finance_db pg_isready -U postgres

echo "Database should be ready now. Testing connection..."
python -m app.db.check_db 