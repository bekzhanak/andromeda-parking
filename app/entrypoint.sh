#!/bin/bash

if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres at $POSTGRES_HOST:$POSTGRES_PORT..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL is available!"
fi

if [ "$COLLECT_STATIC" = "1" ]; then
    echo "Collecting static files..."
    python manage.py collectstatic --no-input --clear
    echo "Static files collected."
fi

echo "Applying database migrations..."
python manage.py migrate
echo "Migrations complete."

echo "Starting Gunicorn server..."
exec gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers 9
