# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-30 19:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_task_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='estimated_hours',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]