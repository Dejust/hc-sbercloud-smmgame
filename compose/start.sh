#!/bin/bash

python manage.py migrate

exec gunicorn --bind 0.0.0.0:8000 -w 1 -k eventlet smmgame2.wsgi runserver 0.0.0.0:8000