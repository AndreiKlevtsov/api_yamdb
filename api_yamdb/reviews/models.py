from django.db import models



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


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genre'
    ),
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='titles'
    )
