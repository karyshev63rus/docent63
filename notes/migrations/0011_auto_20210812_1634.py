# Generated by Django 3.2.4 on 2021-08-12 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0010_slide'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='slide',
            options={'verbose_name': 'слайд', 'verbose_name_plural': 'слайды'},
        ),
        migrations.AlterField(
            model_name='slide',
            name='subtitle',
            field=models.CharField(max_length=50, verbose_name='подзаголовок'),
        ),
        migrations.CreateModel(
            name='SlideTextItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('textItem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slide_items', to='notes.slide', verbose_name='пункт')),
            ],
        ),
    ]
