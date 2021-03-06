# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-22 19:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
        ('products', '0005_auto_20180628_1725'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='Currently in transit', max_length=50)),
                ('Sfname', models.CharField(max_length=50)),
                ('Slname', models.CharField(max_length=50)),
                ('Saddress', models.CharField(max_length=100)),
                ('Scity', models.CharField(max_length=50)),
                ('Sstate', models.CharField(max_length=2)),
                ('Szip', models.CharField(max_length=5)),
                ('Bfname', models.CharField(max_length=50)),
                ('Blname', models.CharField(max_length=50)),
                ('Baddress', models.CharField(max_length=100)),
                ('Bcity', models.CharField(max_length=50)),
                ('Bstate', models.CharField(max_length=2)),
                ('Bzip', models.CharField(max_length=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('items', models.ManyToManyField(related_name='whichorders', to='products.Product')),
                ('placer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='placedorders', to='customers.Customer')),
            ],
        ),
    ]
