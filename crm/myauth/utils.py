from clients.models import Lead
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


def create_group_operators():
    """Create 'operators' group."""
    operators, _ = Group.objects.get_or_create(name="operators")
    per_add_lead = Permission.objects.get(codename="add_lead")
    per_change_lead = Permission.objects.get(codename="change_lead")
    per_delete_lead = Permission.objects.get(codename="delete_lead")
    per_view_lead = Permission.objects.get(codename="view_lead")

    operators.permissions.add(per_add_lead)
    operators.permissions.add(per_change_lead)
    operators.permissions.add(per_delete_lead)
    operators.permissions.add(per_view_lead)

    operators.save()


def create_group_marketers():
    """Create 'marketers' group."""
    marketers, _ = Group.objects.get_or_create(name="marketers")
    per_add_service = Permission.objects.get(codename="add_service")
    per_change_service = Permission.objects.get(codename="change_service")
    per_delete_service = Permission.objects.get(codename="delete_service")
    per_view_service = Permission.objects.get(codename="view_service")

    per_add_advertising = Permission.objects.get(codename="add_advertising")
    per_change_advertising = Permission.objects.get(codename="change_advertising")
    per_delete_advertising = Permission.objects.get(codename="delete_advertising")
    per_view_advertising = Permission.objects.get(codename="view_advertising")

    marketers.permissions.add(per_add_service)
    marketers.permissions.add(per_change_service)
    marketers.permissions.add(per_delete_service)
    marketers.permissions.add(per_view_service)

    marketers.permissions.add(per_add_advertising)
    marketers.permissions.add(per_change_advertising)
    marketers.permissions.add(per_delete_advertising)
    marketers.permissions.add(per_view_advertising)

    marketers.save()


def create_group_managers():
    """Create 'marketers' group."""
    managers, _ = Group.objects.get_or_create(name="managers")
    per_add_contract = Permission.objects.get(codename="add_contract")
    per_change_contract = Permission.objects.get(codename="change_contract")
    per_delete_contract = Permission.objects.get(codename="delete_contract")
    per_view_contract = Permission.objects.get(codename="view_contract")
    per_view_lead = Permission.objects.get(codename="view_lead")

    content_type = ContentType.objects.get_for_model(Lead)
    per_create_customer_from_lead, _ = Permission.objects.get_or_create(
        codename="create_customer_from_lead",
        name="Can create customer from lead",
        content_type=content_type,
    )

    per_add_customer = Permission.objects.get(codename="add_customer")
    per_change_customer = Permission.objects.get(codename="change_customer")
    per_delete_customer = Permission.objects.get(codename="delete_customer")
    per_view_customer = Permission.objects.get(codename="view_customer")

    managers.permissions.add(per_add_contract)
    managers.permissions.add(per_change_contract)
    managers.permissions.add(per_delete_contract)
    managers.permissions.add(per_view_contract)

    managers.permissions.add(per_view_lead)
    managers.permissions.add(per_create_customer_from_lead)

    managers.permissions.add(per_add_customer)
    managers.permissions.add(per_change_customer)
    managers.permissions.add(per_delete_customer)
    managers.permissions.add(per_view_customer)

    managers.save()
