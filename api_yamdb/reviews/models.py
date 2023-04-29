# from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
from django.db import models


# User = get_user_model()


class Category(models.Model):
    name = models.CharField(unique=True, max_length=256,
                            verbose_name='Название')
    slug = models.SlugField(unique=True, max_length=50,
                            verbose_name='Тип категории')

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(unique=True, max_length=256,
                            verbose_name='Жанр')
    slug = models.SlugField(unique=True, max_length=50,
                            verbose_name='slug')

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год')
    description = models.TextField(
        'Описание',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        to_field='slug',
        on_delete=models.PROTECT,
        related_name='titles',
        verbose_name='Категория'
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Название'
    )
    text = models.TextField(
        max_length=200,
        verbose_name='Отзыв',
        help_text='Введите текст отзыва',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.SmallIntegerField(
        verbose_name='Оценка',
        blank=False,
        null=False,
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
        error_messages={
            'validators': 'Оценка от 1 до 10'}
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique review'
            )]
        ordering = ('pub_date',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        help_text='Отзыв, к которому будет относиться этот комментарий'
    )
    text = models.TextField(
        verbose_name='Комментарий',
        help_text='Введите текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'
