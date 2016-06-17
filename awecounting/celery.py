from __future__ import absolute_import

from celery import Celery

app = Celery('awecounting',
             broker='redis://localhost:6379/0',
             backend='redis://localhost',
             include=['awecounting.tasks'])


if __name__ == '__main__':
    app.start()