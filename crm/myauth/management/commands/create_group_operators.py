from django.core.management import BaseCommand
from myauth.utils import create_group_operators


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print("Creating group 'operators'...")
        create_group_operators()
        print("Done")
