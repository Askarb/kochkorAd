# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-24 18:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20171121_1756'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ad',
            options={'ordering': ['-date_update']},
        ),
    ]