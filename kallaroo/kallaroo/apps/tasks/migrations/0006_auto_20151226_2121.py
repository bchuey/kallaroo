# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-26 21:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20151226_1755'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='location',
            table='locations',
        ),
    ]
