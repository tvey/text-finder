from celery import Celery

from src.config import Config


def make_celery():
    celery = Celery(
        'flask-celery-app',
        broker=Config.CELERY_BROKER_URL,
        backend=Config.CELERY_RESULT_BACKEND,
        include=['src.celery_tasks'],
    )
    return celery


celery = make_celery()
# print("tasks={}".format(celery.tasks.keys()))
