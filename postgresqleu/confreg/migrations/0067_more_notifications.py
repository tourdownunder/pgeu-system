# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-02-22 14:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confreg', '0066_attendeemail_addopts'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='notifysessionstatus',
            field=models.BooleanField(default=False, verbose_name='Notify about session status changes by speakers'),
        ),
        migrations.AddField(
            model_name='conference',
            name='notifyvolunteerstatus',
            field=models.BooleanField(default=False, verbose_name='Notify about volunteer schedule changes'),
        ),
    ]
