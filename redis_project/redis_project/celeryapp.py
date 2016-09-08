from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redis_project.settings')


app = Celery('redis_project', broker='redis://localhost:6379/0')
