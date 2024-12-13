from django.core.management import BaseCommand
from myauth.utils import create_group_marketers


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print("Creating group 'marketers'...")
        create_group_marketers()
        print("Done")
