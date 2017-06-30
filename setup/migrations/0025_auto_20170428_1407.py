# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-28 14:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0024_auto_20170426_1842'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='measuredentitybehavior',
            name='measureEntity',
        ),
        migrations.AddField(
            model_name='measuredentitybehavior',
            name='measure_entity',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='behaviors', to='setup.MeasuredEntity'),
            preserve_default=False,
        ),
    ]
