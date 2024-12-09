from datetime import date
from typing import Any, Dict, List, Optional, Tuple

from advertising.models import Advertising
from contracts.models import Contract
from django import forms
from django.forms import ValidationError
from services.models import Service

from .validators import (
    validate_phone_format,
    validate_unique_contract_name,
    validate_unique_email,
    validate_unique_phone,
)


class CustomerBaseForm(forms.Form):
    """
    Base form class for customers.

    The form is used to create an active client from a potential one.
    """

    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput)
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput)
    phone = forms.CharField(
        max_length=20,
        required=True,
        validators=[validate_phone_format],
        widget=forms.TextInput,
    )
    email = forms.EmailField(widget=forms.EmailInput)
    ads = forms.ModelChoiceField(
        queryset=Advertising.objects.all(),
        help_text="the advertising campaign from which the"
        " lead learned about the service",
    )
    name = forms.CharField(
        max_length=100,
        required=True,
        help_text="the unique name of the contract",
        widget=forms.TextInput,
        validators=[validate_unique_contract_name],
    )
    product = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        help_text="the service provided",
    )
    doc = forms.FileField(
        help_text="the file with the contract document",
    )
    end_date = forms.DateField(
        help_text="contract completion date",
        widget=forms.TextInput,
    )
    cost = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        widget=forms.NumberInput,
    )

    def get_data_from_customer_form(self) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Return lead_data and contract_data from CustomerForm."""
        lead_data = {
            "first_name": self.cleaned_data["first_name"],
            "last_name": self.cleaned_data["last_name"],
            "phone": self.cleaned_data["phone"],
            "email": self.cleaned_data["email"],
            "ads": self.cleaned_data["ads"],
        }
        contract_data = {
            "name": self.cleaned_data["name"],
            "product": self.cleaned_data["product"],
            "doc": self.cleaned_data["doc"],
            "end_date": self.cleaned_data["end_date"],
            "cost": self.cleaned_data["cost"],
        }
        return lead_data, contract_data

    def clean(self):
        cleaned_data = super().clean()
        contract_name: Optional[str] = cleaned_data.get("name")
        if not contract_name:
            return cleaned_data

        end_date: date = cleaned_data["end_date"]
        error_msgs: List[str] = []

        contract: Optional[Contract] = Contract.objects.filter(
            name=contract_name
        ).first()
        if contract is None:
            start_date: date = date.today()
        else:
            start_date = contract.start_date

        if start_date >= end_date:
            error_msgs.append(
                f"The end date must not be less than the start date ({start_date})."
            )

        if error_msgs:
            raise ValidationError(" & ".join(error_msgs))
        return cleaned_data


class NewCustomerForm(CustomerBaseForm):
    """
    Form for creating a new active client.

    The phone field has validators for uniqueness and the correct format;
     the email field has a validator for uniqueness
    """

    phone = forms.CharField(
        max_length=20,
        required=True,
        validators=[validate_unique_phone, validate_phone_format],
        widget=forms.TextInput,
    )
    email = forms.EmailField(
        widget=forms.EmailInput, validators=[validate_unique_email]
    )


class CustomerUpdateForm(CustomerBaseForm):
    """
    Form for updating the active client.

    The name field has not validators;
     the email field has not validators
    """

    name = forms.CharField(
        max_length=100,
        required=True,
        help_text="the unique name of the contract",
        widget=forms.TextInput,
        validators=[],
    )
    email = forms.EmailField(widget=forms.EmailInput, validators=[])
