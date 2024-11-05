from __future__ import absolute_import, unicode_literals
import os
from KarAmooziRoshan.celery import Celery
from datasets.task import generate_report_task

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KarAmooziRoshan.settings")

app = Celery("KarAmooziRoshan")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(86400.0, generate_report_task.s(), name="call every 24 hours")
