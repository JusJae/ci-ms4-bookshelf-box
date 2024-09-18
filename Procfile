release: ./install_setuptools.sh && python manage.py migrate && python manage.py load_subscription_options subscriptions/fixtures/subscription_options.json 
web: ./install_setuptools.sh && gunicorn bookshelf_box.wsgi:application
