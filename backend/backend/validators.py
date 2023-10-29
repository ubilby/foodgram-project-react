import re

from django.core.exceptions import ValidationError


def validate_positive(value):
    if value <= 0:
        raise ValidationError("Field's value should be greater than 0")


def username_validator(value):
    unmatched = re.sub(r'^[\w.@+-]+\Z', '', value)
    if value == "me":
        raise ValidationError("Name cant contain me")
    elif value in unmatched:
        raise ValidationError(
            f'Name cant contain me {unmatched}'
        )
    return value
