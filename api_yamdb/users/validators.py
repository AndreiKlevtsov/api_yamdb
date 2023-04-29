from django.core.exceptions import ValidationError


def validate_username(value):
    invalid_username = ['me', '-', '.', '!']
    if value in invalid_username:
        raise ValidationError(
            ('Имя пользователя содержит недопустимые символы'),
            params={'value': value},
        )
