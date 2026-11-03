#!/bin/sh
set -eu
: "${RD_TOKEN:?definir RD_TOKEN d'abord}"
curl -fsS -H "X-Rundeck-Auth-Token: $RD_TOKEN" \
  "http://localhost:4440/api/41/project/veille/jobs/export?format=yaml" \
  -o rundeck/jobs/veille-jobs.yaml
echo "Jobs exportes dans rundeck/jobs/veille-jobs.yaml"
