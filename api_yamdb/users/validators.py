import re

from django.core.exceptions import ValidationError


def validate_username(value):
    """
    Проверяет, что username пользователя != 'me'.
    """
    REGEX = r'^[\w.@+-]'
    if value == 'me':
        raise ValidationError(
            (f'{value} не может быть <me>.'),
            params={'value': value},
        )
    if not re.match(REGEX, value):
        raise ValidationError(
            (f'{value} не соотвествует допустимому формату.'),
            params={'value': value},
        )
