# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-27 20:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='tagline',
            field=models.CharField(default='enter a tagline', max_length=255),
        ),
    ]
