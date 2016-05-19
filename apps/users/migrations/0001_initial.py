# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import njango.fields
import django.contrib.auth.models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0001_initial'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('username', models.CharField(unique=True, max_length=50)),
                ('full_name', models.CharField(max_length=245)),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name=b'email address', db_index=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'swappable': 'AUTH_USER_MODEL',
            },
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('is_party', models.BooleanField(default=False, verbose_name=b'Also create party for a branch')),
            ],
            options={
                'verbose_name_plural': 'Branches',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('location', models.TextField()),
                ('organization_type', models.CharField(default=b'sole_proprietorship', max_length=254, choices=[(b'sole_proprietorship', b'Sole Proprietorship'), (b'partnership', b'Partnership'), (b'corporation', b'Corporation'), (b'non_profit', b'Non-profit')])),
                ('tax_registration_number', models.IntegerField(null=True, blank=True)),
                ('sells_goods', models.BooleanField(default=True)),
                ('sells_services', models.BooleanField(default=False)),
                ('purchases_goods', models.BooleanField(default=True)),
                ('purchases_services', models.BooleanField(default=True)),
                ('use_nepali_fy_system', models.BooleanField(default=True)),
                ('fy_start_month', models.PositiveIntegerField(default=1)),
                ('fy_start_day', models.PositiveIntegerField(default=12)),
                ('enable_bs', models.BooleanField(default=True, verbose_name=b'Enable BS Calendar')),
                ('enable_multi_language', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attachment', models.FileField(null=True, upload_to=b'cheque_payments/%Y/%m/%d', blank=True)),
                ('description', models.TextField(max_length=254, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=100)),
                ('date', njango.fields.BSDateField(null=True, blank=True)),
                ('company', models.ForeignKey(related_name='pin', to='users.Company')),
                ('used_by', models.ForeignKey(related_name='used_pin', blank=True, to='users.Company', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company', models.ForeignKey(related_name='roles', to='users.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enable_purchase', models.BooleanField(default=True)),
                ('enable_purchase_order', models.BooleanField(default=True)),
                ('enable_sales', models.BooleanField(default=True)),
                ('enable_cash_vouchers', models.BooleanField(default=True)),
                ('enable_journal_voucher', models.BooleanField(default=True)),
                ('enable_fixed_assets_voucher', models.BooleanField(default=True)),
                ('enable_bank_vouchers', models.BooleanField(default=True)),
                ('enable_share_management', models.BooleanField(default=True)),
                ('enable_payroll', models.BooleanField(default=True)),
                ('enable_reports', models.BooleanField(default=True)),
                ('company', models.OneToOneField(related_name='subscription', to='users.Company')),
            ],
        ),
        migrations.CreateModel(
            name='GroupProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Group',
                'proxy': True,
            },
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.AddField(
            model_name='role',
            name='group',
            field=models.ForeignKey(related_name='roles', to='auth.Group'),
        ),
        migrations.AddField(
            model_name='role',
            name='user',
            field=models.ForeignKey(related_name='roles', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='branch',
            name='branch_company',
            field=models.ForeignKey(blank=True, to='users.Company', null=True),
        ),
        migrations.AddField(
            model_name='branch',
            name='company',
            field=models.ForeignKey(related_name='branches', to='users.Company'),
        ),
        migrations.AddField(
            model_name='branch',
            name='party',
            field=models.ForeignKey(blank=True, to='ledger.Party', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(related_name='users', to='auth.Group', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='role',
            unique_together=set([('user', 'group', 'company')]),
        ),
        migrations.AlterUniqueTogether(
            name='pin',
            unique_together=set([('company', 'used_by')]),
        ),
    ]
