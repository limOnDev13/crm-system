from typing import Any, Dict, Tuple

from advertising.models import Advertising
from clients.validators import validate_phone
from django import forms
from services.models import Service


class CustomerForm(forms.Form):
    """Form class for customers."""

    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput)
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput)
    phone = forms.CharField(
        max_length=20,
        required=True,
        validators=[validate_phone],
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
