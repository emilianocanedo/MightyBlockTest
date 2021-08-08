#!/usr/bin/env sh

set -ex

TRY_LOOP="2"

wait_for_port() {
  local name="$1" host="$2" port="$3"
  local j=0
  while ! nc -z "$host" "$port" >/dev/null 2>&1 < /dev/null; do
    j=$((j+1))
    if [ $j -ge $TRY_LOOP ]; then
      echo >&2 "$(date) - $host:$port still not reachable, giving up"
      exit 1
    fi
    echo "$(date) - waiting for $name... $j/$TRY_LOOP"
    sleep 5
  done
}

# Exports DB Migrations
cd /model
# Some items in the model import settings, but alembic doesn't need any of that
touch settings.py

if [ ! -d 'alembic' ]
then
  alembic init alembic
fi
cp ../exports_alembic.ini ./alembic.ini
wait_for_port postgres postgres 6667
alembic upgrade head

rm settings.py
