# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0001_initial'),
        ('ledger', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='worktimevoucher',
            name='company',
            field=models.ForeignKey(to='users.Company'),
        ),
        migrations.AddField(
            model_name='workday',
            name='work_time_voucher_row',
            field=models.ForeignKey(related_name='work_days', to='payroll.WorkTimeVoucherRow'),
        ),
        migrations.AddField(
            model_name='individualpayroll',
            name='company',
            field=models.ForeignKey(to='users.Company'),
        ),
        migrations.AddField(
            model_name='individualpayroll',
            name='employee',
            field=models.ForeignKey(to='payroll.Employee'),
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
            model_name='grouppayrollrow',
            name='employee',
            field=models.ForeignKey(to='payroll.Employee'),
        ),
        migrations.AddField(
            model_name='grouppayrollrow',
            name='group_payroll',
            field=models.ForeignKey(related_name='rows', to='payroll.GroupPayroll'),
        ),
        migrations.AddField(
            model_name='grouppayrollrow',
            name='pay_head',
            field=models.ForeignKey(to='ledger.Account'),
        ),
        migrations.AddField(
            model_name='grouppayroll',
            name='company',
            field=models.ForeignKey(to='users.Company'),
        ),
        migrations.AddField(
            model_name='entryrow',
            name='employee',
            field=models.ForeignKey(to='ledger.Account'),
        ),
        migrations.AddField(
            model_name='entryrow',
            name='entry',
            field=models.ForeignKey(related_name='rows', to='payroll.Entry'),
        ),
        migrations.AddField(
            model_name='entryrow',
            name='pay_heading',
            field=models.ForeignKey(related_name='row', to='ledger.Account'),
        ),
        migrations.AddField(
            model_name='entry',
            name='company',
            field=models.ForeignKey(to='users.Company'),
        ),
        migrations.AddField(
            model_name='employee',
            name='account',
            field=models.OneToOneField(null=True, to='ledger.Account'),
        ),
        migrations.AddField(
            model_name='employee',
            name='company',
            field=models.ForeignKey(to='users.Company'),
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
            name='company',
            field=models.ForeignKey(to='users.Company'),
        ),
        migrations.AddField(
            model_name='attendancevoucher',
            name='employee',
            field=models.ForeignKey(to='payroll.Employee'),
        ),
    ]
