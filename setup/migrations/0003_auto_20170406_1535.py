# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-06 15:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0002_auto_20170404_1542'),
    ]

    operations = [
        migrations.RenameField(
            model_name='iosignalsdevicetype',
            old_name='I_O',
            new_name='i_o',
        ),
        migrations.AddField(
            model_name='inputoutputport',
            name='behavior_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='inputoutputport',
            name='transformation_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='monitoringdevice',
            name='descr',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='monitoringdevice',
            name='ip_address',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='monitoringdevice',
            name='mac_address',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='monitoringdevice',
            name='serial',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
