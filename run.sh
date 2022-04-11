#!/bin/bash
echo "running backend"
nohup python manage.py runserver 0.0.0.0:8000> /dev/null 2>&1 & exit
