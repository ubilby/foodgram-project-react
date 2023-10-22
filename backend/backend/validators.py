from django.core.exceptions import ValidationError


def validate_positive(value):
    if value <= 0:
        raise ValidationError("Field's value should be greater than 0")
