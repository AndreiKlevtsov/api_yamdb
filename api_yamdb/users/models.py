from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from .validators import validate_username


class CustomUserManager(UserManager):
    """
    При создании superuser присваивает роль Administrator.
    """

    def create_superuser(self, username, email=None, password=None,
                         **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.ADMIN)
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLES = [
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Administrator'),
    ]
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        validators=(validate_username,)

    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True,
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
    objects = CustomUserManager()

    def create_super(self, request):
        if request.user.is_admin:
            self.role = self.ADMIN

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return (self.role == self.ADMIN
                or self.is_superuser)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
