#!/bin/bash

rm -rf */migrations
rm -rf */__pycache__
rm -rf */*/__pycache__
rm -rf */*/*/__pycache__


python3 manage.py makemigrations
python3 manage.py makemigrations customer

python3 manage.py migrate
python3 manage.py collectstatic
#python3 manage.py runserver 127.0.0.1:7000
python3 manage.py runserver 0.0.0.0:7000

