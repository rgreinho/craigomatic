#!/bin/bash

# Ensure the DB is up and running before starting Django.
>&2 echo -n "Starting Celery Flower."
until psql -h "db" -U "postgres" -c '\l'; do
  sleep 1
  >&2 echo -n .
done

# Migrate db, so we have the latest db schema.
python manage.py migrate

# Start development server on public ip interface, on port 8000.
exec gunicorn -b 0.0.0.0:8000 craigomatic.wsgi
