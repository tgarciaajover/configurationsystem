# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-06 21:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0010_signaltype_last_updttm'),
    ]

    operations = [
        migrations.AddField(
            model_name='signalunit',
            name='last_updttm',
            field=models.DateTimeField(auto_now=True, verbose_name='last datetime'),
        ),
        migrations.AlterField(
            model_name='signalunit',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='create date'),
        ),
    ]
