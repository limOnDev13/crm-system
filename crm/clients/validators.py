import re

from django.core.exceptions import ValidationError


def validate_phone(value: str):
    """Phone validator."""
    # phone must have format +7 (999) 000 0000
    if not re.match(r"\+7 \(\d{3}?\) \d{3}? \d{4}?", value):
        raise ValidationError(
            "Phone must have format +7 (999) 000 0000", params={"phone": value}
        )
