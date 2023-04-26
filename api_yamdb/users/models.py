from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOISES = (
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin')
    )
    role = models.CharField(
        choices=ROLE_CHOISES,
        default='User',
        blank=True,
        help_text='Права доступа пользователя'
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=155,
        unique=True,
        blank=False,
        null=False,
    )
    email = models.CharField(
        verbose_name='Электронная почта',
        max_length=155,
        unique=True,
        blank=False,
        null=False,
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=155,
        unique=False,
        blank=True,
        null=True,
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

