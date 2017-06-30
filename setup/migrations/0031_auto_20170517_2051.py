# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-17 20:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0030_auto_20170508_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='displaytype',
            name='letter_size',
            field=models.CharField(choices=[('0', 'Normal 5 (5X5)'), ('1', 'Normal 7 (6X7)'), ('2', 'Normal 14 (8X14)'), ('3', 'Normal 15 (9X15)'), ('4', 'Normal 16 (9X16)')], default='1', max_length=1),
        ),
    ]
