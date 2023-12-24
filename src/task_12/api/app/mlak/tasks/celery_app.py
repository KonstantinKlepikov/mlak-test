import os
from celery import Celery


CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")


celery_app = Celery(
    "worker",
    beiker=CELERY_BROKER_URL,
    include=['mlak.tasks', ],
        )
