#!/bin/bash

rm -rfv */migrations
rm -rfv */__pycache__
rm -rfv */*/__pycache__
rm -rfv */*/*/__pycache__


python3 manage.py makemigrations commons
python3 manage.py makemigrations customer
python3 manage.py makemigrations product
python3 manage.py makemigrations home
#python3 manage.py makemigrations

python3 manage.py migrate 
#python3 manage.py migrate customer
#python3 manage.py migrate product

python3 manage.py collectstatic
#python3 manage.py runserver 127.0.0.1:7000
python3 manage.py runserver 0.0.0.0:7000

