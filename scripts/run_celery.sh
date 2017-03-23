#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

cd appcinema
# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
su -m myuser -c "export DJANGO_SETTINGS_MODULE=appcinema.settings"
su -m myuser -c "echo $DJANGO_SETTINGS_MODULE"
su -m myuser -c "celery worker -A appcinema.celery -l info"