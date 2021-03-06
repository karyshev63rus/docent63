# Generated by Django 3.2.4 on 2021-08-12 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0012_auto_20210812_1649'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='slide',
            options={'ordering': ('title',), 'verbose_name': 'слайд', 'verbose_name_plural': 'слайды'},
        ),
        migrations.AlterField(
            model_name='slide',
            name='subtitle',
            field=models.CharField(blank=True, max_length=50, verbose_name='подзаголовок'),
        ),
        migrations.AlterField(
            model_name='slide',
            name='title',
            field=models.CharField(blank=True, max_length=50, verbose_name='заголовок'),
        ),
        migrations.AlterField(
            model_name='slidetextitem',
            name='text',
            field=models.CharField(blank=True, max_length=50, verbose_name='позиция'),
        ),
    ]
