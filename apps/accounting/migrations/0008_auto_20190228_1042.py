# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-02-28 16:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0007_auto_20181111_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),

    ]
