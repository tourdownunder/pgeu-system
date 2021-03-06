# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-01-25 13:06
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JobHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('success', models.BooleanField()),
                ('runtime', models.DurationField()),
                ('output', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ScheduledJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=200)),
                ('command', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('enabled', models.BooleanField(default=True)),
                ('notifyonsuccess', models.BooleanField(default=False, verbose_name="Notify on success", help_text="Send notification email even if job is successful")),
                ('nextrun', models.DateTimeField(blank=True, null=True)),
                ('lastrun', models.DateTimeField(blank=True, null=True)),
                ('lastrunsuccess', models.BooleanField(default=False)),
                ('lastskip', models.DateTimeField(blank=True, null=True)),
                ('scheduled_times', django.contrib.postgres.fields.ArrayField(base_field=models.TimeField(), blank=True, null=True, size=None)),
                ('scheduled_interval', models.DurationField(blank=True, null=True)),
                ('override_times', django.contrib.postgres.fields.ArrayField(base_field=models.TimeField(), blank=True, help_text='Specify a comma separated list of times (hour:minute:second) to override the default schedule', null=True, size=None)),
                ('override_interval', models.DurationField(blank=True, help_text='Specify an interval (hours:minutes:seconds) to override the default schedule', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SchedulerConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hold_all_jobs', models.BooleanField(default=False)),
            ],
        ),
        migrations.RunSQL(
            "ALTER TABLE scheduler_schedulerconfig ADD CONSTRAINT highlander CHECK (id=1)",
        ),
        migrations.RunSQL(
            "INSERT INTO scheduler_schedulerconfig (hold_all_jobs) VALUES (false)",
        ),
        migrations.AlterUniqueTogether(
            name='scheduledjob',
            unique_together=set([('app', 'command')]),
        ),
        migrations.AddField(
            model_name='jobhistory',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduler.ScheduledJob'),
        ),
    ]
