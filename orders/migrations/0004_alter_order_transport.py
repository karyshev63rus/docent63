# Generated by Django 3.2.4 on 2021-08-03 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20210802_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='transport',
            field=models.CharField(choices=[('Courier delivery', 'Courier delivery'), ('Recipient pickup', 'Recipient pickup')], max_length=20, verbose_name='условия доставки'),
        ),
    ]
