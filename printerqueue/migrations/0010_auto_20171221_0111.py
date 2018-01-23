# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-12-21 01:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('printerqueue', '0009_auto_20171220_2314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='queueobject',
            name='end_timedate',
        ),
        migrations.RemoveField(
            model_name='queueobject',
            name='reserved_time',
        ),
        migrations.RemoveField(
            model_name='queueobject',
            name='start_timedate',
        ),
        migrations.AddField(
            model_name='queue',
            name='allowed_time_end',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='queue',
            name='allowed_time_start',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='queue',
            name='include_description',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='queueobject',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='queueobject',
            name='end',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='queueobject',
            name='start',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]