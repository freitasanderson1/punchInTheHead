pipenv --python 3.12

pipenv run python manage.py collectstatic --noinput
pipenv run python manage.py makemigrations --noinput
pipenv run python manage.py migrate --noinput

# pipenv run python manage.py shell -c "django.contrib.auth.models import User; \
#     User.objects.filter(username='admin').exists() or \
#     User.objects.create_superuser('admin',
#     'admin@example.com', 'senha123');"
    
./runDocker