# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-23 23:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contractor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=255)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('joined_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'contractors',
            },
        ),
        migrations.CreateModel(
            name='ContractorProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('rating', models.IntegerField(default=1)),
                ('contractor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.Contractor')),
            ],
            options={
                'db_table': 'contractor_profiles',
            },
        ),
    ]