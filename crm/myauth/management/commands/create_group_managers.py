from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand
from django.contrib.contenttypes.models import ContentType

from clients.models import Lead


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print("Creating group 'managers'...")
        managers, _ = Group.objects.get_or_create(
            name="managers"
        )
        per_add_contract = Permission.objects.get(
            codename="add_contract"
        )
        per_change_contract = Permission.objects.get(
            codename="change_contract"
        )
        per_delete_contract = Permission.objects.get(
            codename="delete_contract"
        )
        per_view_contract = Permission.objects.get(
            codename="view_contract"
        )
        per_view_lead = Permission.objects.get(
            codename="view_lead"
        )

        content_type = ContentType.objects.get_for_model(Lead)
        per_create_customer_from_lead, _ = Permission.objects.get_or_create(
            codename="create_customer_from_lead",
            name="Can create customer from lead",
            content_type=content_type,
        )

        managers.permissions.add(per_add_contract)
        managers.permissions.add(per_change_contract)
        managers.permissions.add(per_delete_contract)
        managers.permissions.add(per_view_contract)
        managers.permissions.add(per_view_lead)
        managers.permissions.add(per_create_customer_from_lead)

        managers.save()
        print("Done")
