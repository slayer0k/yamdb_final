# Generated by Django 2.2.16 on 2022-09-24 12:58

import reviews.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20220923_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveSmallIntegerField(help_text='Дата издания произведения', validators=[reviews.validators.check_year], verbose_name='Дата издания'),
        ),
    ]
