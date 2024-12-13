from typing import Optional, Tuple

from django.db import IntegrityError

from .forms import CustomerUpdateForm


def integrity_error_parser(
    exc: IntegrityError, form: CustomerUpdateForm
) -> Tuple[Optional[str], str]:
    """
    Parse the text of the IntegrityError.

    :param exc: IntegrityError
    :param form: The form for changing the active client.
    :return: Field name (or None if there is no field name in the error text)
     and DETAIL of IntegrityError
    """
    exc_text: str = str(exc).split("DETAIL:")[1]
    for field in form:
        if field.name in str(exc):
            return field.name, exc_text
    return None, exc_text
