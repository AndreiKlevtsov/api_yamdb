from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        validators=(validate_username, )
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,

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
        verbose_name='Роль',
        max_length=10,
        choices=ROLES,
        default=USER,
        blank=True,
        help_text='Права доступа пользователя'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
