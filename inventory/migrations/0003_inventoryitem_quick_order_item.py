# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-20 01:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20171029_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='quick_order_item',
            field=models.BooleanField(default=False),
        ),
    ]