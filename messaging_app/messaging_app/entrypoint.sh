#!/bin/sh

# Default values
: "${MYSQL_HOST:=${DATABASE_HOST:-mysql-service}}"
: "${MYSQL_PORT:=${DATABASE_PORT:-3306}}"

# Wait for the database to be ready
echo "Waiting for database..."
while ! nc -z "$MYSQL_HOST" "$MYSQL_PORT"; do
    sleep 0.5
done

echo "Database is up!"

# The CMD from the Dockerfile will be executed here
exec "$@"