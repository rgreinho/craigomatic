#!/bin/bash

# Gets the Celery command, defaults to worker.
CELERY_COMMAND=${1:-worker}

# Wait for the django service to run to ensure the migrations were performed.
echo -n "Starting Celery ${CELERY_COMMAND}."
while ! curl --output /dev/null --silent --head --fail http://django:8000; do
    sleep 1
    echo -n .
done;

# Start Celery command.
DATE=$(date -u +%Y-%m-%dT%H%M%S%Z)
exec su -m celery -c "celery ${CELERY_COMMAND} -A craigomatic -l info --pidfile=celery_worker-${DATE}.pid"
