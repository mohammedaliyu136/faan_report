# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-10-21 22:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0002_auto_20181021_1850'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Row_data',
        ),
        migrations.AlterField(
            model_name='tabledata',
            name='month_d',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='tabledata',
            name='quater_d',
            field=models.CharField(default='nodate', max_length=25),
        ),
        migrations.AlterField(
            model_name='tabledata',
            name='year_d',
            field=models.CharField(default='nodate', max_length=25),
        ),
    ]
