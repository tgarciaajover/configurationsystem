# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-05-16 21:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0053_auto_20190516_1548'),
    ]

    operations = [
        migrations.RenameField(
            model_name='measuredentityoperator',
            old_name='maquina',
            new_name='measured_entity',
        ),
    ]
