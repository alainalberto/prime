# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-14 03:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id_apl', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('fullname', models.CharField(max_length=20)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=10, null=True)),
                ('no_social', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(max_length=255)),
                ('license_numb', models.CharField(blank=True, max_length=45, null=True)),
                ('usdot', models.CharField(blank=True, max_length=25, null=True)),
                ('mc', models.CharField(blank=True, max_length=25, null=True)),
                ('txdmv', models.CharField(blank=True, max_length=25, null=True)),
                ('ein', models.CharField(blank=True, max_length=25, null=True)),
                ('service', models.CharField(blank=True, max_length=255, null=True)),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
                ('date_view', models.DateTimeField(blank=True, null=True)),
                ('state', models.CharField(blank=True, max_length=20, null=True)),
                ('update', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Audit',
            fields=[
                ('id_aud', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(blank=True, max_length=20, null=True)),
                ('auditor_name', models.CharField(blank=True, max_length=100, null=True)),
                ('action_plan', models.BooleanField(default=False)),
                ('amount_paid', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('state', models.CharField(blank=True, max_length=20, null=True)),
                ('results', models.CharField(blank=True, max_length=255, null=True)),
                ('update', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id_con', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('serial', models.CharField(blank=True, max_length=20, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('state', models.CharField(blank=True, max_length=20, null=True)),
                ('type', models.CharField(blank=True, max_length=20, null=True)),
                ('update', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerHasAlert',
            fields=[
                ('id_cal', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id_drv', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('license_numb', models.CharField(blank=True, max_length=45, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('lic_date_exp', models.DateField(blank=True, null=True)),
                ('medicard_date_exp', models.DateField(blank=True, null=True)),
                ('drugtest_date', models.DateField(blank=True, null=True)),
                ('drugtest_date_exp', models.DateField(blank=True, null=True)),
                ('mbr_date', models.DateField(blank=True, null=True)),
                ('mbr_date_exp', models.DateField(blank=True, null=True)),
                ('begining_date', models.DateField(blank=True, null=True)),
                ('deactivate', models.BooleanField(default=False)),
                ('deactivate_date', models.DateField(blank=True, null=True)),
                ('state', models.CharField(blank=True, max_length=20, null=True)),
                ('update', models.DateField(blank=True, null=True)),
                ('customers', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounting.Customer')),
                ('users', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id_tru', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(blank=True, max_length=45, null=True)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('model', models.CharField(blank=True, max_length=45, null=True)),
                ('serial', models.CharField(blank=True, max_length=20, null=True)),
                ('number', models.IntegerField(blank=True, null=True)),
                ('plate_date_exp', models.DateField(blank=True, null=True)),
                ('title_date_reg', models.DateField(blank=True, null=True)),
                ('title_date_exp_reg', models.DateField(blank=True, null=True)),
                ('title_date_insp', models.DateField(blank=True, null=True)),
                ('title_date_exp_insp', models.DateField(blank=True, null=True)),
                ('state', models.CharField(blank=True, max_length=20, null=True)),
                ('update', models.DateField(blank=True, null=True)),
                ('deactivate', models.BooleanField(default=False)),
                ('deactivate_date', models.DateField(blank=True, null=True)),
                ('customers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.Customer')),
                ('users', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ifta',
            fields=[
                ('id_ift', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(auto_now_add=True)),
                ('type', models.CharField(blank=True, max_length=45, null=True)),
                ('period', models.CharField(blank=True, max_length=45, null=True)),
                ('nex_period', models.DateField(blank=True, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('payment_due', models.DateField(blank=True, null=True)),
                ('state', models.CharField(blank=True, max_length=20, null=True)),
                ('update', models.DateField(blank=True, null=True)),
                ('customers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.Customer')),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id_ins', models.AutoField(primary_key=True, serialize=False)),
                ('down_payment', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('policy_efective_date', models.DateField(blank=True, null=True)),
                ('policy_date_exp', models.DateField(blank=True, null=True)),
                ('policy_cargo_exp', models.DateField(blank=True, null=True)),
                ('policy_physical_exp', models.DateField(blank=True, null=True)),
                ('liability', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('policy_liability', models.CharField(blank=True, max_length=100, null=True)),
                ('cargo', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('cargo_policy', models.CharField(blank=True, max_length=100, null=True)),
                ('physical_damage', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('physical_damg_policy', models.CharField(blank=True, max_length=100, null=True)),
                ('sale_type', models.CharField(blank=True, max_length=20, null=True)),
                ('sale_date_fee', models.DateField(blank=True, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('comision', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('paid_out', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('balance_due', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('state', models.CharField(blank=True, max_length=20, null=True)),
                ('update', models.DateField(blank=True, null=True)),
                ('monthlypay', models.DateField(blank=True, null=True)),
                ('note', models.CharField(blank=True, max_length=250, null=True)),
                ('other_description', models.CharField(blank=True, max_length=45, null=True)),
                ('other', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('other_policy', models.CharField(blank=True, max_length=100, null=True)),
                ('policy_other_exp', models.DateField(blank=True, null=True)),
                ('customers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.Customer')),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Permit',
            fields=[
                ('id_com', models.AutoField(primary_key=True, serialize=False)),
                ('is_new', models.BooleanField(default=True)),
                ('legal_status', models.CharField(blank=True, max_length=10, null=True)),
                ('gusiness_type', models.CharField(blank=True, max_length=45, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('attorney', models.CharField(blank=True, max_length=100, null=True)),
                ('otheattorney', models.CharField(blank=True, max_length=45, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=10, null=True)),
                ('othephone', models.CharField(blank=True, max_length=10, null=True)),
                ('fax', models.CharField(blank=True, max_length=10, null=True)),
                ('ein', models.CharField(blank=True, max_length=20, null=True)),
                ('created_date', models.DateField(blank=True, null=True)),
                ('unit', models.IntegerField(blank=True, null=True)),
                ('usdot', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
                ('usdot_pin', models.CharField(blank=True, max_length=20, null=True)),
                ('txdmv', models.CharField(blank=True, max_length=20, null=True)),
                ('txdmv_user', models.CharField(blank=True, max_length=20, null=True)),
                ('txdmv_passd', models.CharField(blank=True, max_length=45, null=True)),
                ('txdmv_date', models.DateField(blank=True, null=True)),
                ('txdmv_date_exp', models.DateField(blank=True, null=True)),
                ('mc', models.CharField(blank=True, max_length=20, null=True)),
                ('mc_pin', models.CharField(blank=True, max_length=20, null=True)),
                ('boc3', models.BooleanField(default=False)),
                ('boc3_date', models.DateField(blank=True, null=True)),
                ('ucr', models.BooleanField(default=False)),
                ('ucr_date_exp', models.DateField(blank=True, null=True)),
                ('account_number', models.CharField(blank=True, max_length=45, null=True)),
                ('account_user', models.CharField(blank=True, max_length=45, null=True)),
                ('account_password', models.CharField(blank=True, max_length=45, null=True)),
                ('inter', models.BooleanField(default=False)),
                ('state', models.CharField(blank=True, max_length=20, null=True)),
                ('update', models.DateField(blank=True, null=True)),
                ('deactivate', models.BooleanField(default=False)),
                ('deactivate_date', models.DateField(blank=True, null=True)),
                ('customers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.Customer')),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
