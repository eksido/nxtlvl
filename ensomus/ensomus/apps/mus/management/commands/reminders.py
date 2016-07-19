from django.core.management.base import BaseCommand, CommandError
from ensomus.apps.mus.models import *
from django.utils.timezone import now
from datetime import timedelta, datetime
from django_mailer_plus import send_mail
import warnings
import exceptions
# from ensomus.ensomus.apps.mus.models import ReminderTemplate

__author__ = 'tl'


class Command(BaseCommand):
    args = 'lol'
    help = 'Check and send out reminders'

    def debug(self, msg):
        print('{} - {}'.format(datetime.utcnow(), msg))

    def handle(self, *args, **options):
        self.debug('Handling reminders command')

        # self.createMockups()

        # django_mailer_plus isnt's set up for timezone aware datetimes
        # so i'm filtering that warning out. (Dont have time right now to
        # fix django_mailer_plus)
        warnings.filterwarnings(
            "ignore",
            category=exceptions.RuntimeWarning,
            module='django.db.models.fields',
            lineno=903
        )

        pending = Reminder.getPending()

        for reminder in pending:
            """ @type reminder Reminder"""
            self.debug('Sending id:' + str(reminder.pk))
            reminder.send()

        self.debug('Done')
