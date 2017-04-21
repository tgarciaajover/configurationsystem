# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-21 00:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canonical', '0002_auto_20170420_1847'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grupomaquina',
            name='compania',
        ),
        migrations.RemoveField(
            model_name='grupomaquina',
            name='planta',
        ),
        migrations.RemoveField(
            model_name='grupomaquina',
            name='sede',
        ),
        migrations.RemoveField(
            model_name='maquina',
            name='compania',
        ),
        migrations.RemoveField(
            model_name='maquina',
            name='grupo_maquina',
        ),
        migrations.RemoveField(
            model_name='maquina',
            name='planta',
        ),
        migrations.RemoveField(
            model_name='maquina',
            name='sede',
        ),
        migrations.RemoveField(
            model_name='ordenproduccionplaneada',
            name='compania',
        ),
        migrations.RemoveField(
            model_name='ordenproduccionplaneada',
            name='grupo_maquina',
        ),
        migrations.RemoveField(
            model_name='ordenproduccionplaneada',
            name='maquina',
        ),
        migrations.RemoveField(
            model_name='ordenproduccionplaneada',
            name='planta',
        ),
        migrations.RemoveField(
            model_name='ordenproduccionplaneada',
            name='sede',
        ),
        migrations.RemoveField(
            model_name='paradaplaneada',
            name='compania',
        ),
        migrations.RemoveField(
            model_name='paradaplaneada',
            name='grupo_maquina',
        ),
        migrations.RemoveField(
            model_name='paradaplaneada',
            name='maquina',
        ),
        migrations.RemoveField(
            model_name='paradaplaneada',
            name='planta',
        ),
        migrations.RemoveField(
            model_name='paradaplaneada',
            name='sede',
        ),
        migrations.RemoveField(
            model_name='planproduccion',
            name='compania',
        ),
        migrations.RemoveField(
            model_name='planproduccion',
            name='grupo_maquina',
        ),
        migrations.RemoveField(
            model_name='planproduccion',
            name='maquina',
        ),
        migrations.RemoveField(
            model_name='planproduccion',
            name='planta',
        ),
        migrations.RemoveField(
            model_name='planproduccion',
            name='sede',
        ),
        migrations.RemoveField(
            model_name='planta',
            name='compania',
        ),
        migrations.RemoveField(
            model_name='planta',
            name='sede',
        ),
        migrations.RemoveField(
            model_name='razonparada',
            name='compania',
        ),
        migrations.RemoveField(
            model_name='razonparada',
            name='planta',
        ),
        migrations.RemoveField(
            model_name='razonparada',
            name='sede',
        ),
        migrations.RemoveField(
            model_name='sede',
            name='compania',
        ),
        migrations.AddField(
            model_name='grupomaquina',
            name='id_compania',
            field=models.CharField(default='0', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grupomaquina',
            name='id_planta',
            field=models.CharField(default='0', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grupomaquina',
            name='id_sede',
            field=models.CharField(default='0', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='maquina',
            name='id_compania',
            field=models.CharField(default='0', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='maquina',
            name='id_grupo_maquina',
            field=models.CharField(default='0', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='maquina',
            name='id_planta',
            field=models.CharField(default='0', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='maquina',
            name='id_sede',
            field=models.CharField(default='0', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ordenproduccionplaneada',
            name='id_compania',
            field=models.CharField(default='0', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ordenproduccionplaneada',
            name='id_grupo_maquina',
            field=models.CharField(default='0', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ordenproduccionplaneada',
            name='id_maquina',
            field=models.CharField(default='0', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ordenproduccionplaneada',
            name='id_planta',
            field=models.CharField(default='0', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ordenproduccionplaneada',
            name='id_sede',
            field=models.CharField(default='0', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paradaplaneada',
            name='id_compania',
            field=models.CharField(default='0', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paradaplaneada',
            name='id_grupo_maquina',
            field=models.CharField(default='0', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paradaplaneada',
            name='id_maquina',
            field=models.CharField(default='0', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paradaplaneada',
            name='id_planta',
            field=models.CharField(default='0', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paradaplaneada',
            name='id_sede',
            field=models.CharField(default='0', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planproduccion',
            name='id_compania',
            field=models.CharField(default='0', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planproduccion',
            name='id_grupo_maquina',
            field=models.CharField(default='0', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planproduccion',
            name='id_maquina',
            field=models.CharField(default='0', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planproduccion',
            name='id_planta',
            field=models.CharField(default='0', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planproduccion',
            name='id_sede',
            field=models.CharField(default='0', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planta',
            name='id_compania',
            field=models.CharField(default='0', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planta',
            name='id_sede',
            field=models.CharField(default='0', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='razonparada',
            name='id_compania',
            field=models.CharField(default='0', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='razonparada',
            name='id_planta',
            field=models.CharField(default='0', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='razonparada',
            name='id_sede',
            field=models.CharField(default='0', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sede',
            name='id_compania',
            field=models.CharField(default='0', max_length=60),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ordenproduccionplaneada',
            name='ano',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='ordenproduccionplaneada',
            name='mes',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='ordenproduccionplaneada',
            name='num_horas',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='paradaplaneada',
            name='ano',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='paradaplaneada',
            name='mes',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='planproduccion',
            name='ano',
            field=models.IntegerField(choices=[(1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017)], default=2017, verbose_name='ano'),
        ),
        migrations.AlterField(
            model_name='planproduccion',
            name='mes',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11)], default=4, verbose_name='mes'),
        ),
    ]
