# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-01 20:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_auto_20180218_1904'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='phone',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='insurance',
            name='months',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dispatchload',
            name='prefix',
            field=models.CharField(default='invl', max_length=4),
        ),
        migrations.AlterField(
            model_name='dispatchload',
            name='start_date',
            field=models.DateField(default='2018-11-01'),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='monthlypay',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
