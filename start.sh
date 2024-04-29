python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py runserver 0.0.0.0:5000

#sh -c "gunicorn --bind 0.0.0.0:8000 app.wsgi"