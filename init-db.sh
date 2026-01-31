#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE p1_as2_db;
    CREATE DATABASE p2_as2_db;
    GRANT ALL PRIVILEGES ON DATABASE p1_as2_db TO postgres;
    GRANT ALL PRIVILEGES ON DATABASE p2_as2_db TO postgres;
EOSQL

echo "Databases p1_as2_db and p2_as2_db created successfully"
