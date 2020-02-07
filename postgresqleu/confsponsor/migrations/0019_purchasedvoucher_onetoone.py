# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-02-07 16:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('confsponsor', '0018_contract_storage_inline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchasedvoucher',
            name='batch',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='confreg.PrepaidBatch'),
        ),
    ]
