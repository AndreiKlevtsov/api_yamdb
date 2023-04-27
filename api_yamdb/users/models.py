from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    ROLE_CHOISES = (
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin')
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        validators=(validate_username, )
    )
    email = models.CharField(
        verbose_name='Электронная почта',
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=155,
        unique=True,
        blank=False,
        null=False,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=155,
        unique=True,
        blank=False,
        null=False,
    )
    bio = models.TextField(
        verbose_name='О себе',
        blank=True,
        null=True,
        help_text='О себе',
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOISES,
        default='User',
        blank=True,
        help_text='Права доступа пользователя'
    )
