# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-05-13 15:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canonical', '0004_auto_20190503_0906'),
    ]

    operations = [
        migrations.AddField(
            model_name='maquina',
            name='tiempo_refresco',
            field=models.IntegerField(default=5),
        ),
    ]
