from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print("Creating group 'operators'...")
        operators, _ = Group.objects.get_or_create(
            name="operators"
        )
        per_add_lead = Permission.objects.get(
            codename="add_lead"
        )
        per_change_lead = Permission.objects.get(
            codename="change_lead"
        )
        per_delete_lead = Permission.objects.get(
            codename="delete_lead"
        )
        per_view_lead = Permission.objects.get(
            codename="view_lead"
        )

        operators.permissions.add(per_add_lead)
        operators.permissions.add(per_change_lead)
        operators.permissions.add(per_delete_lead)
        operators.permissions.add(per_view_lead)

        operators.save()
        print("Done")
