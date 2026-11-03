#!/bin/sh
set -eu
psql "$VEILLE_DB_DSN" -v ON_ERROR_STOP=1 -f /opt/veille/sql/ingest.sql
