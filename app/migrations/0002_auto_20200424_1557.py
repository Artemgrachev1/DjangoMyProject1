# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-04-24 12:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2020, 4, 24, 15, 57, 47, 79730), verbose_name='Опубликована'),
        ),
    ]