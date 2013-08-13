from django.core.management.base import NoArgsCommand
from django.db import connection

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        try:
            self.email_tasks()
        except Exception as e:
            print(e)
        finally:
            connection.close()

    def email_tasks(self):
        print("test() just fired!!")
