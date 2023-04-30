from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            ('Имя пользователя не может быть <me>.'),
            params={'value': value},
        )


class MyValidator(UnicodeUsernameValidator):
    # regex = r'^[\w.@+-]+\+z'
    #       r'^[\w.@+\- ]+$'
    pass



regex_validator = MyValidator()
