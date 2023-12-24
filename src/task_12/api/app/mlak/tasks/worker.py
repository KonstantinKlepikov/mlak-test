import requests
from typing import Any
from mlak.tasks.celery_app import celery_app

import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from mlak.models import Books


EXT_ENPOINT = 'https://fakerapi.it/api/v1/books?_quantity=1'


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        60.0,
        query_and_save.s(),
        name='Ask a new book'
            )


@celery_app.task
def query_and_save() -> dict[str, Any]:
    """Query data and save it to db periodic
    """
    q = requests.get(EXT_ENPOINT)
    if q.status_code == 200:
        result = q.json()["data"][0]
        del result['id']
        b = Books(**result)
        b.save()
        return result
