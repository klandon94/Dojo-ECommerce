# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-28 21:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20180628_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='none.jpg', upload_to='media/{self.category}'),
        ),
    ]
