#!/bin/sh
set -e

# wait-for-db is implemented by attempting migrations until it's reachable
echo "Waiting for DB..."
until python manage.py migrate --noinput; do
  echo "DB unavailable - sleeping"
  sleep 1
done

echo "Creating admin user..."
python manage.py create_admin

echo "Collectstatic..."
python manage.py collectstatic --noinput || true

# Start server
gunicorn streaming_backend.wsgi:application --bind 0.0.0.0:8000