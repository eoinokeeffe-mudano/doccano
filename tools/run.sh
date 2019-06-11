#!/usr/bin/env bash

set -o errexit

# set environment variables
export OAUTH_GOOGLE2_KEY=$1
export OUTH_GOOGLE2_SECRET=$2
export DOCCANO_DB_NAME=$3
export DOCCANO_DB_USER=$4
export DOCCANO_DB_PASSWD=$5
export DOCCANO_DB_HOST=$6
export DOCCANO_DB_PORT=$7

if [[ ! -d "app/staticfiles" ]]; then python app/manage.py collectstatic --noinput; fi

python app/manage.py wait_for_db
python app/manage.py migrate
gunicorn --bind="0.0.0.0:${PORT:-8000}" --workers="${WORKERS:-1}" --pythonpath=app app.wsgi --timeout 300
