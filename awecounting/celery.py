from __future__ import absolute_import
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'awecounting.settings')

app = Celery('awecounting',
             broker='redis://localhost:6379/0',
             backend='redis://localhost',
             include=['awecounting.tasks'])


if __name__ == '__main__':
    app.start()