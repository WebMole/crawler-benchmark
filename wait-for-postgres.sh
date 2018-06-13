#!/bin/bash

set -e

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST"  -d"$POSTGRES_DB"  -U "$POSTGRES_USER" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping - $POSTGRES_PASSWORD - $POSTGRES_HOST"
  sleep 1
done

echo "Postgres is up - executing command: $@"

exec $@
