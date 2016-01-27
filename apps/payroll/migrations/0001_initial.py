# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20160124_1529'),
        ('ledger', '0008_auto_20160106_1434'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceVoucher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('total_working_days', models.FloatField(null=True, blank=True)),
                ('full_present_day', models.FloatField(null=True, blank=True)),
                ('half_present_day', models.FloatField(null=True, blank=True)),
                ('half_multiplier', models.FloatField(default=0.5, null=True, blank=True)),
                ('early_late_attendance_day', models.FloatField(null=True, blank=True)),
                ('early_late_multiplier', models.FloatField(default=1, null=True, blank=True)),
                ('total_ot_hours', models.FloatField(null=True, blank=True)),
                ('paid', models.BooleanField(default=False)),
                ('company', models.ForeignKey(to='users.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Deduction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('address', models.TextField(null=True, blank=True)),
                ('tax_id', models.CharField(max_length=100, null=True, blank=True)),
                ('designation', models.CharField(max_length=100, null=True, blank=True)),
                ('account', models.OneToOneField(null=True, to='ledger.Account')),
                ('company', models.ForeignKey(to='users.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entry_no', models.CharField(max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(to='users.Company')),
            ],
        ),
        migrations.CreateModel(
            name='EntryRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.IntegerField()),
                ('amount', models.FloatField()),
                ('hours', models.FloatField()),
                ('tax', models.FloatField()),
                ('remarks', models.TextField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(to='ledger.Account')),
                ('entry', models.ForeignKey(related_name='rows', to='payroll.Entry')),
                ('pay_heading', models.ForeignKey(related_name='row', to='ledger.Account')),
            ],
        ),
        migrations.CreateModel(
            name='GroupPayroll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('status', models.CharField(default=b'Unapproved', max_length=10, choices=[(b'Approved', b'Approved'), (b'Unapproved', b'Unapproved')])),
                ('company', models.ForeignKey(to='users.Company')),
            ],
        ),
        migrations.CreateModel(
            name='GroupPayrollRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rate_day', models.FloatField(null=True, blank=True)),
                ('rate_hour', models.FloatField(null=True, blank=True)),
                ('rate_ot_hour', models.FloatField(null=True, blank=True)),
                ('payroll_tax', models.FloatField(null=True, blank=True)),
                ('employee', models.ForeignKey(to='payroll.Employee')),
                ('group_payroll', models.ForeignKey(related_name='rows', to='payroll.GroupPayroll')),
                ('pay_head', models.ForeignKey(to='ledger.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Inclusion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='IndividualPayroll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('day_rate', models.FloatField(null=True, blank=True)),
                ('hour_rate', models.FloatField(null=True, blank=True)),
                ('ot_hour_rate', models.FloatField(null=True, blank=True)),
                ('status', models.CharField(default=b'Unapproved', max_length=10, choices=[(b'Approved', b'Approved'), (b'Unapproved', b'Unapproved')])),
                ('company', models.ForeignKey(to='users.Company')),
                ('employee', models.ForeignKey(to='payroll.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='WorkDay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('in_time', models.TimeField()),
                ('out_time', models.TimeField()),
                ('day', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='WorkTimeVoucher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('company', models.ForeignKey(to='users.Company')),
            ],
        ),
        migrations.CreateModel(
            name='WorkTimeVoucherRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('paid', models.BooleanField(default=False)),
                ('employee', models.ForeignKey(to='payroll.Employee')),
                ('work_time_voucher', models.ForeignKey(related_name='rows', to='payroll.WorkTimeVoucher')),
            ],
        ),
        migrations.AddField(
            model_name='workday',
            name='work_time_voucher_row',
            field=models.ForeignKey(related_name='work_days', to='payroll.WorkTimeVoucherRow'),
        ),
        migrations.AddField(
            model_name='inclusion',
            name='individual_payroll',
            field=models.ForeignKey(related_name='inclusions', to='payroll.IndividualPayroll'),
        ),
        migrations.AddField(
            model_name='inclusion',
            name='particular',
            field=models.ForeignKey(to='ledger.Account'),
        ),
        migrations.AddField(
            model_name='deduction',
            name='individual_payroll',
            field=models.ForeignKey(related_name='deductions', to='payroll.IndividualPayroll'),
        ),
        migrations.AddField(
            model_name='deduction',
            name='particular',
            field=models.ForeignKey(to='ledger.Account'),
        ),
        migrations.AddField(
            model_name='attendancevoucher',
            name='employee',
            field=models.ForeignKey(to='payroll.Employee'),
        ),
    ]
