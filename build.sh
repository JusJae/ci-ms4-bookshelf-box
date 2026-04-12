#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py load_subscription_options subscriptions/fixtures/subscription_options.json
gunicorn bookshelf_box.wsgi:application