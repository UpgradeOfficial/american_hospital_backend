import logging
from time import sleep

from celery import shared_task
from django.conf import settings


class Task:
    def __init__(self, f):
        self.f = f

    def delay(self, *args, **kwargs):
        logging.debug(f"Task started with params {args}, {kwargs}")
        return self.f(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)


def my_shared_task(f):
    task = Task(f)
    t = (
        task if settings.CELERY_TEST_ACTIVE is True else shared_task(f)
    )  # Testing shared task
    return t


@my_shared_task
def test_task(time):
    sleep(time)
    return f"This slept for {time}"
