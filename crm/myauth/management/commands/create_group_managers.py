from django.core.management import BaseCommand
from myauth.utils import create_group_managers


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print("Creating group 'managers'...")
        create_group_managers()
        print("Done")
