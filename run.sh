#!/bin/bash
DIR=/home/admin

time=`date -d "now" +%Y-%m-%d-%H-%M`
mv $DIR/django.log $DIR/django_log/django$time.log

ps -aux | grep manage.py | grep -v grep | awk '{print $2}' | xargs kill -9

echo "running backend"
nohup python manage.py runserver 0.0.0.0:8000> $DIR/django.log 2>&1 & exit
