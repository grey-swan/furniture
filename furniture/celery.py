from __future__ import absolute_import, unicode_literals
import os

from datetime import timedelta
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'furniture.settings')

app = Celery('furniture')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# 添加定时任务
app.conf.update(
    CELERYBEAT_SCHEDULE = {
        'cycle-task': {
            'task': 'product.tasks.task_deal_access_token',
            # 'schedule': crontab(day_of_month=1, hour=0, minute=0),
            'schedule': timedelta(seconds=7000),
        },
    }
)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
