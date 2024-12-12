from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print("Creating group 'marketers'...")
        marketers, _ = Group.objects.get_or_create(
            name="marketers"
        )
        per_add_service = Permission.objects.get(
            codename="add_service"
        )
        per_change_service = Permission.objects.get(
            codename="change_service"
        )
        per_delete_service = Permission.objects.get(
            codename="delete_service"
        )
        per_view_service = Permission.objects.get(
            codename="view_service"
        )

        per_add_advertising = Permission.objects.get(
            codename="add_advertising"
        )
        per_change_advertising = Permission.objects.get(
            codename="change_advertising"
        )
        per_delete_advertising = Permission.objects.get(
            codename="delete_advertising"
        )
        per_view_advertising = Permission.objects.get(
            codename="view_advertising"
        )

        marketers.permissions.add(per_add_service)
        marketers.permissions.add(per_change_service)
        marketers.permissions.add(per_delete_service)
        marketers.permissions.add(per_view_service)

        marketers.permissions.add(per_add_advertising)
        marketers.permissions.add(per_change_advertising)
        marketers.permissions.add(per_delete_advertising)
        marketers.permissions.add(per_view_advertising)

        marketers.save()
        print("Done")
