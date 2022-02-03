from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celeryProduct.settings')

app = Celery('celeryProduct')
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')


app.autodiscover_tasks()

# Celery Beat Settings
app.conf.beat_schedule = {
    'testing_task': {
        'task': 'csvToModel.tasks.csvToModeldata',
        'schedule':crontab(minute=32, hour=15, day_of_week='*',day_of_month="*"),
    },
    
}

app.conf.timezone = 'Asia/Kolkata' 


# celery -A celeryProduct worker -B