# Generated by Django 3.2 on 2023-04-26 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_alter_title_year'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={},
        ),
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='titles', to='reviews.category', to_field='slug', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
    ]
