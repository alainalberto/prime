# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-14 03:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id_acn', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('primary', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='AccountDescrip',
            fields=[
                ('id_acd', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(blank=True, max_length=20, null=True)),
                ('document', models.IntegerField()),
                ('date', models.DateField(auto_now_add=True)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('waytopay', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id_cut', models.AutoField(primary_key=True, serialize=False)),
                ('fullname', models.CharField(max_length=50)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=10, null=True)),
                ('no_social', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(max_length=255)),
                ('deactivated', models.BooleanField(default=False)),
                ('date_deactivated', models.DateField(blank=True, null=True)),
                ('usdot', models.CharField(blank=True, max_length=20, null=True)),
                ('mc', models.CharField(blank=True, max_length=20, null=True)),
                ('txdmv', models.CharField(blank=True, max_length=20, null=True)),
                ('ein', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id_emp', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('lastname', models.CharField(blank=True, max_length=45, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('social_no', models.CharField(blank=True, max_length=20, null=True)),
                ('date_admis', models.DateField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=10, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('type_salary', models.CharField(blank=True, max_length=20, null=True)),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('position', models.CharField(blank=True, max_length=20, null=True)),
                ('deactivated', models.BooleanField(default=False)),
                ('date_deactivated', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeHasPayment',
            fields=[
                ('id_pym', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('id_fee', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(blank=True, max_length=20, null=True)),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id_inv', models.AutoField(primary_key=True, serialize=False)),
                ('serial', models.IntegerField()),
                ('type', models.CharField(blank=True, max_length=20, null=True)),
                ('start_date', models.DateField(default='2018-02-14')),
                ('subtotal', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('waytopay', models.CharField(max_length=20)),
                ('discount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('comission_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('wire_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('ach_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('prefix', models.CharField(default='inv', max_length=4)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('note', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceLoad',
            fields=[
                ('id_inv', models.AutoField(primary_key=True, serialize=False)),
                ('biller', models.CharField(blank=True, max_length=45, null=True)),
                ('biller_address', models.CharField(blank=True, max_length=100, null=True)),
                ('biller_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('serial', models.IntegerField()),
                ('type', models.CharField(blank=True, max_length=20, null=True)),
                ('start_date', models.DateField(default='2018-02-14')),
                ('subtotal', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('waytopay', models.CharField(max_length=20)),
                ('discount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('comission_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('wire_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('ach_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('prefix', models.CharField(default='inv', max_length=4)),
                ('end_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='InvoicesHasItem',
            fields=[
                ('id_ind', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
                ('tax', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id_ite', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('note', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id_sal', models.AutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('pay_date', models.DateField(blank=True, default='2018-02-14', null=True)),
                ('serial', models.CharField(blank=True, max_length=20, null=True)),
                ('regular_hours', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('overtime_hours', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('discount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('gross', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('waytopay', models.CharField(max_length=20)),
                ('note', models.CharField(blank=True, max_length=250, null=True)),
                ('paid', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id_rec', models.AutoField(primary_key=True, serialize=False)),
                ('serial', models.CharField(max_length=20)),
                ('start_date', models.DateField(default='2018-02-14')),
                ('end_date', models.DateField(blank=True, null=True)),
                ('description', models.CharField(max_length=45)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('waytopay', models.CharField(max_length=20)),
                ('paid', models.BooleanField(default=True)),
                ('accounts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.Account')),
            ],
        ),
    ]
