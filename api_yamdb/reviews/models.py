from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User
from django.db import models


class Title(models.Model):
    pass


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Название'
    )
    text = models.TextField(
        verbose_name='Отзыв',
        help_text='Введите текст отзыва',
        blank=False,
        null=False,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        blank=True,
        null=True,
        verbose_name='Автор'
    )
    score = models.SmallIntegerField(verbose_name='Оценка',
                                     validators=(
                                         MinValueValidator(1),
                                         MaxValueValidator(10)
                                     ),
                                     blank=False,
                                     null=False,
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
                fields=['author', 'title'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.title


class Comment(models.Model):
    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        related_name='comment',
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
