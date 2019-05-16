# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-05-16 20:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0052_measuredattributevalue_measuringentitystatusinterval'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeasuredEntityOperator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maquina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.MeasuredEntity')),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.Operator')),
            ],
        ),
        migrations.RemoveField(
            model_name='machineoperator',
            name='operator',
        ),
        migrations.DeleteModel(
            name='MachineOperator',
        ),
    ]
