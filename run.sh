#!/bin/bash
echo "running backend"
nohup python manage.py runserver 0.0.0.0:8000> /home/admin/django.log 2>&1 & exit
