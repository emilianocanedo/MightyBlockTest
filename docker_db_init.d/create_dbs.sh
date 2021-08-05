#!/bin/bash
set -ex

function create_db() {
  local database=$1
  psql -v ON_ERROR_STOP=1 --username dbadmin <<-EOSQL
    CREATE USER $database PASSWORD '$database';
    CREATE DATABASE $database;
    GRANT ALL PRIVILEGES ON DATABASE $database TO $database;
EOSQL
}

if [ -n "POSTGRES_MULTIPLE_DATABASES" ]; then
  echo "Creating databases for $POSTGRES_USER: $POSTGRES_MULTIPLE_DATABASES"
  for db in $(echo $POSTGRES_MULTIPLE_DATABASES | tr ',' ' '); do
    create_db $db
  done
  echo "Databases created"
fi