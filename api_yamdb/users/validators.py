from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError


def validate_username(value):
    """
    Проверяет, что username пользователя != 'me'.
    """
    if value == 'me':
        raise ValidationError(
            ('Имя пользователя не может быть <me>.'),
            params={'value': value},
        )


class MyValidator(UnicodeUsernameValidator):
    pass


unicode_validator = MyValidator()
