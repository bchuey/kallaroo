# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-05 20:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20160105_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='braintree_client_token',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]