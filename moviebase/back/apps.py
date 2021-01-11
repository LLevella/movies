from django.apps import AppConfig
import django_rq
from collections import defaultdict
from .tasks import db_relocator
import datetime


class BackConfig(AppConfig):
    name = 'back'

    def ready(self):
        scheduler = django_rq.get_scheduler('default')

        # Delete any existing jobs in the scheduler when the app starts up
        for job in scheduler.get_jobs():
            job.delete()

        # Have 'db_relocation' run every 15 minutes
        scheduler.schedule(datetime.datetime.now(datetime.timezone.utc),
                           db_relocator, interval=60*15)
