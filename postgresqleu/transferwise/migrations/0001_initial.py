# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-03-26 15:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('invoices', '0013_vatcache'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransferwiseRefund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refundid', models.BigIntegerField(unique=True)),
                ('uuid', models.UUIDField(unique=True)),
                ('transferid', models.BigIntegerField(unique=True)),
                ('accid', models.BigIntegerField(null=True)),
                ('quoteid', models.BigIntegerField(null=True)),
                ('createdat', models.DateTimeField(auto_now_add=True)),
                ('completedat', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TransferwiseTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twreference', models.CharField(max_length=100)),
                ('datetime', models.DateTimeField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('feeamount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('transtype', models.CharField(max_length=32)),
                ('paymentref', models.CharField(blank=True, max_length=200)),
                ('fulldescription', models.CharField(blank=True, max_length=500)),
                ('counterpart_name', models.CharField(blank=True, max_length=100)),
                ('counterpart_account', models.CharField(blank=True, max_length=100)),
                ('counterpart_valid_iban', models.BooleanField(default=False)),
                ('paymentmethod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoices.InvoicePaymentMethod')),
            ],
            options={
                'ordering': ('-datetime',),
            },
        ),
        migrations.AddField(
            model_name='transferwiserefund',
            name='origtransaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refund_orig', to='transferwise.TransferwiseTransaction'),
        ),
        migrations.AddField(
            model_name='transferwiserefund',
            name='refundtransaction',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='refund_refund', to='transferwise.TransferwiseTransaction'),
        ),
        migrations.AlterUniqueTogether(
            name='transferwisetransaction',
            unique_together=set([('twreference', 'paymentmethod')]),
        ),
    ]
