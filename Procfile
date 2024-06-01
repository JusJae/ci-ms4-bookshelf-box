web: gunicorn bookshelf_box.wsgi:application
release: python manage.py migrate && python manage.py load_subscription_options subscriptions/fixtures/subscription_options.json