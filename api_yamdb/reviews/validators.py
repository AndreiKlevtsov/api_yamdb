from datetime import date

from django.core.exceptions import ValidationError


def validate_year(value):
    """
    Проверяет, что значение поля year не превышает текущий год.
    """
    if value > date.today().year:
        raise ValidationError(
            'Нельзя указывать год, который больше текущего.'
        )
