#!/bin/bash
set -e

# Commands to get feature_requester up and running.
python manage.py drop_db
python manage.py create_db
python manage.py init_db
gunicorn manage:app

exec "$@"