# django-rest-framework-project
 Apis
set up project
django -admin start project
cd project
django -admin startapp apis
python -m venv env
venv\scripits\activate
pip install django
pip install djangorestframework
pip install markdown
pip install django-filter
python manage.py makemigrations
python manage.py migrate
python manage.py create superuser


changesin settings.py

1) APIVIEW decorator
 which takes list of http methods that the view respond to
@api_view['GET','POST','PUT','DELETE']

