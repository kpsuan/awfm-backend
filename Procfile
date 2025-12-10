web: gunicorn awfm.wsgi --bind 0.0.0.0:$PORT
release: python manage.py migrate && python manage.py seed_data
