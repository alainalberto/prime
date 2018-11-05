# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-18 19:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessHasLoad',
            fields=[
                ('id_bsl', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerHasLoad',
            fields=[
                ('id_csl', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Diesel',
            fields=[
                ('id_dse', models.AutoField(primary_key=True, serialize=False)),
                ('date_start', models.DateField(blank=True, null=True)),
                ('date_end', models.DateField(blank=True, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('moves', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DispatchHasPayment',
            fields=[
                ('id_pym', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='DispatchLoadHasLoad',
            fields=[
                ('id_inl', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='DispatchLogt',
            fields=[
                ('id_dsp', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=45, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('comission', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('deactivate', models.BooleanField(default=False)),
                ('date_deactivated', models.DateTimeField(blank=True, null=True)),
                ('prefix', models.CharField(default='invl', max_length=4)),
                ('start_date', models.DateField(default='2018-11-01')),
            ],
        ),
        migrations.CreateModel(
            name='DriversHasPayment',
            fields=[
                ('id_pym', models.AutoField(primary_key=True, serialize=False)),
                ('company_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('porc_company', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('pre_pass', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('escrow', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('down_payment', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('insurance', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('diesel', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('other', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_driver', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_owner', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DriversLogt',
            fields=[
                ('id_dr', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=45, null=True)),
                ('ssn', models.CharField(blank=True, max_length=10, null=True)),
                ('owner_name', models.CharField(blank=True, max_length=75, null=True)),
                ('license_numb', models.CharField(max_length=45)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(max_length=100)),
                ('dob', models.DateField(blank=True, null=True)),
                ('lic_date_exp', models.DateField(blank=True, null=True)),
                ('medicard_date_exp', models.DateField(blank=True, null=True)),
                ('drugtest_date', models.DateField(blank=True, null=True)),
                ('drugtest_date_exp', models.DateField(blank=True, null=True)),
                ('mbr_date', models.DateField(blank=True, null=True)),
                ('mbr_date_exp', models.DateField(blank=True, null=True)),
                ('begining_date', models.DateField(blank=True, null=True)),
                ('deactivate', models.BooleanField(default=False)),
                ('date_deactivated', models.DateTimeField(blank=True, null=True)),
                ('type', models.CharField(max_length=45)),
                ('dow_payment', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('escrow', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('phone', models.TextField(blank=True, max_length=25, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IftaLogt',
            fields=[
                ('id_ift', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(blank=True, null=True)),
                ('state', models.CharField(blank=True, max_length=45, null=True)),
                ('milles', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
                ('gallons', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='InsuranceLogt',
            fields=[
                ('id_inr', models.AutoField(primary_key=True, serialize=False)),
                ('down_payment', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('pilicy_efective_date', models.DateField(blank=True, null=True)),
                ('pilicy_date_exp', models.DateField(blank=True, null=True)),
                ('liability', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('pilicy_liability', models.CharField(blank=True, max_length=45, null=True)),
                ('cargo', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('cargo_pilicy', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('physical_damage', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('physical_damg_pilicy', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('sale_type', models.CharField(blank=True, max_length=20, null=True)),
                ('sale_date_fee', models.DateField(blank=True, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
                ('fee_value', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
                ('paid', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='InvoicesHasLoad',
            fields=[
                ('id_inl', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Load',
            fields=[
                ('id_lod', models.AutoField(primary_key=True, serialize=False)),
                ('broker', models.CharField(blank=True, max_length=45, null=True)),
                ('pickup_from', models.CharField(blank=True, max_length=45, null=True)),
                ('pickup_date', models.DateField(blank=True, null=True)),
                ('deliver', models.CharField(blank=True, max_length=45, null=True)),
                ('deliver_date', models.DateField(blank=True, null=True)),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('number', models.CharField(blank=True, max_length=20, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('other_company', models.BooleanField(default=False)),
                ('note', models.CharField(blank=True, max_length=225, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LoadsHasFee',
            fields=[
                ('id_lfe', models.AutoField(primary_key=True, serialize=False)),
                ('value', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentHasLoad',
            fields=[
                ('id_pyl', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='PermissionsLogt',
            fields=[
                ('id_prm', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(blank=True, null=True)),
                ('usdot', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('usdot_pin', models.CharField(blank=True, max_length=20, null=True)),
                ('txdmv', models.CharField(blank=True, max_length=20, null=True)),
                ('txdmv_user', models.CharField(blank=True, max_length=20, null=True)),
                ('txdmv_passd', models.CharField(blank=True, max_length=45, null=True)),
                ('txdmv_date', models.DateField(blank=True, null=True)),
                ('txdmv_date_exp', models.DateField(blank=True, null=True)),
                ('mc', models.CharField(blank=True, max_length=20, null=True)),
                ('mc_pin', models.CharField(blank=True, max_length=20, null=True)),
                ('boc3', models.BooleanField(default=True)),
                ('boc3_date', models.DateField(blank=True, null=True)),
                ('ucr', models.BooleanField(default=True)),
                ('update', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TravelExpense',
            fields=[
                ('id_tre', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('value', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TrucksLogt',
            fields=[
                ('id_tuk', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(blank=True, max_length=45, null=True)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('model', models.CharField(blank=True, max_length=45, null=True)),
                ('serial', models.CharField(blank=True, max_length=20, null=True)),
                ('number', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
                ('insp_date_exp', models.DateField(blank=True, null=True)),
                ('regit_date_exp', models.DateField(blank=True, null=True)),
                ('deactivate', models.BooleanField(default=False)),
                ('deactivate_date', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
