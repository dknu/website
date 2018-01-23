# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-11-22 01:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('printerqueue', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='queue',
            options={'permissions': ('can_create_queue', 'Can create queue')},
        ),
        migrations.AlterField(
            model_name='queue',
            name='description',
            field=models.TextField(default=' No description'),
        ),
        migrations.AlterField(
            model_name='queueobject',
            name='end_timedate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='queueobject',
            name='queue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='queueobjects', to='printerqueue.Queue'),
        ),
        migrations.AlterField(
            model_name='queueobject',
            name='reserved_time',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='queueobject',
            name='start_timedate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='queueobject',
            name='submitted_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]