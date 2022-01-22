from celery import shared_task
from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger
import requests, os, django
from django.core import management


@shared_task
def add(x, y):
    return x + y

@shared_task
def get_exchange_rate():
    management.member('Command', '--noinput', '--remove-empty-dirs')
    return "Done"