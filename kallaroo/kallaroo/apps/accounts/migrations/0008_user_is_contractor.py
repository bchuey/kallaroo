# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-29 22:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_contractor_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_contractor',
            field=models.BooleanField(default=False),
        ),
    ]
