from typing import Optional

from contracts.models import Contract
from django.core.exceptions import ValidationError

from .models import Lead


def validate_unique_phone(value: str) -> None:
    """Validate that phone is unique."""
    lead = Lead.objects.filter(phone=value).first()
    if lead is not None:
        raise ValidationError("Phone already exists", params={"phone": value})


def validate_unique_contract_name(value: str) -> None:
    """Validate that contract name is unique."""
    contract = Contract.objects.filter(name=value).first()
    if contract is not None:
        raise ValidationError("Contract name already exists", params={"name": value})


def validate_unique_email(value: str) -> None:
    """Validate that email is unique."""
    lead: Optional[Lead] = Lead.objects.filter(email=value).first()
    if lead is not None:
        raise ValidationError("Email already exists", params={"email": value})
