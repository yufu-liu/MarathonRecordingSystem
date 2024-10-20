import time
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError

class Command(BaseCommand):
    """Django command to wait for database to be available"""

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_conn = None
        attempts = 0
        while not db_conn:
            try:
                db_conn = connections['default']
                self.stdout.write(self.style.SUCCESS('Database available!'))
            except OperationalError:
                attempts += 1
                if attempts > 10:
                    self.stdout.write(self.style.ERROR('Database not available after 10 attempts. Exiting.'))
                    exit(1)
                self.stdout.write('Database unavailable, waiting 5 seconds...')
                time.sleep(5)