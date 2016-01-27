from django.db import models
from awecounting.utils.helpers import zero_for_none
from apps.ledger.models import Account
from apps.users.models import Company
from njango.fields import BSDateField, today
from django.core.urlresolvers import reverse_lazy
from awecounting.utils.helpers import get_next_voucher_no


class Entry(models.Model):
    entry_no = models.CharField(max_length=10)
    company = models.ForeignKey(Company)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse_lazy('entry_edit', kwargs={'pk': self.id})

    def __init__(self, *args, **kwargs):
        super(Entry, self).__init__(*args, **kwargs)

        if not self.pk and not self.entry_no:
            self.entry_no = get_next_voucher_no(Entry, self.company_id, attr='entry_no')

    @property
    def total(self):
        grand_total = 0
        for obj in self.rows.all():
            total = obj.amount
            grand_total += total
        return grand_total


class EntryRow(models.Model):
    sn = models.IntegerField()
    employee = models.ForeignKey(Account)
    pay_heading = models.ForeignKey(Account, related_name='row')
    amount = models.FloatField()
    hours = models.FloatField()
    tax = models.FloatField()
    remarks = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    entry = models.ForeignKey(Entry, related_name='rows')

    def get_absolute_url(self):
        return self.entry.get_absolute_url()


class Employee(models.Model):
    name = models.CharField(max_length=254)
    address = models.TextField(null=True, blank=True)
    tax_id = models.CharField(max_length=100, null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    account = models.OneToOneField(Account, null=True)
    company = models.ForeignKey(Company)

    def set_paid(self):
        attendance_vouchers = AttendanceVoucher.objects.filter(employee=self, paid=False)
        for voucher in attendance_vouchers:
            voucher.paid = True
            voucher.save()
        work_time_voucher_rows = WorkTimeVoucherRow.objects.filter(employee=self, paid=False)
        for row in work_time_voucher_rows:
            row.paid = True
            row.save()

    def get_unpaid_days(self):
        total = 0
        attendance_vouchers = AttendanceVoucher.objects.filter(employee=self, paid=False)
        for voucher in attendance_vouchers:
            total += zero_for_none(voucher.total_present_days())
        return total

    def get_unpaid_hours(self):
        total = 0
        work_time_voucher_rows = WorkTimeVoucherRow.objects.filter(employee=self, paid=False)
        for row in work_time_voucher_rows:
            for work_day in row.work_days.all():
                total += zero_for_none(work_day.work_minutes())
        return round(float(total) / 60, 2)

    def get_unpaid_ot_hours(self):
        total = 0
        attendance_vouchers = AttendanceVoucher.objects.filter(employee=self, paid=False)
        for voucher in attendance_vouchers:
            total += zero_for_none(voucher.total_ot_hours)
        return total

    def save(self, *args, **kwargs):
        if self.pk is None:
            super(Employee, self).save(*args, **kwargs)
            account = Account(code='13-0001-' + str(self.id), name=self.name)
            account.company = self.company
            account.add_category('Employee')
            account.save()
            self.account = account
        super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class AttendanceVoucher(models.Model):
    voucher_no = models.CharField(max_length=50)
    date = models.DateField()
    employee = models.ForeignKey(Employee)
    from_date = models.DateField()
    to_date = models.DateField()
    total_working_days = models.FloatField(null=True, blank=True)
    full_present_day = models.FloatField(null=True, blank=True)
    half_present_day = models.FloatField(null=True, blank=True)
    half_multiplier = models.FloatField(default=0.5, null=True, blank=True)
    early_late_attendance_day = models.FloatField(null=True, blank=True)
    early_late_multiplier = models.FloatField(default=1, null=True, blank=True)
    total_ot_hours = models.FloatField(null=True, blank=True)
    paid = models.BooleanField(default=False)
    company = models.ForeignKey(Company)

    def total_present_days(self):
        return self.full_present_day + self.half_present_day * self.half_multiplier + self.early_late_attendance_day * self.early_late_multiplier


class WorkTimeVoucher(models.Model):
    voucher_no = models.CharField(max_length=50)
    date = models.DateField()
    from_date = models.DateField()
    to_date = models.DateField()
    company = models.ForeignKey(Company)


class WorkTimeVoucherRow(models.Model):
    employee = models.ForeignKey(Employee)
    paid = models.BooleanField(default=False)
    work_time_voucher = models.ForeignKey(WorkTimeVoucher, related_name='rows')


class WorkDay(models.Model):
    in_time = models.TimeField()
    out_time = models.TimeField()
    work_time_voucher_row = models.ForeignKey(WorkTimeVoucherRow, related_name='work_days')
    day = models.DateField()

    def get_in_time(self):
        hms = str(self.in_time)
        pieces = hms.split(':')
        hm = pieces[0] + ':' + pieces[1]
        return hm

    def get_out_time(self):
        hms = str(self.out_time)
        pieces = hms.split(':')
        hm = pieces[0] + ':' + pieces[1]
        return hm

    def work_minutes(self):
        in_hour = self.in_time.hour
        out_hour = self.out_time.hour
        if in_hour > out_hour:
            out_hour += 24
        return (out_hour - in_hour) * 60 + self.out_time.minute - self.in_time.minute


class GroupPayroll(models.Model):
    voucher_no = models.CharField(max_length=50)
    date = models.DateField()
    company = models.ForeignKey(Company)
    statuses = [('Approved', 'Approved'), ('Unapproved', 'Unapproved')]
    status = models.CharField(max_length=10, choices=statuses, default='Unapproved')


class GroupPayrollRow(models.Model):
    employee = models.ForeignKey(Employee)
    rate_day = models.FloatField(null=True, blank=True)
    rate_hour = models.FloatField(null=True, blank=True)
    rate_ot_hour = models.FloatField(null=True, blank=True)
    payroll_tax = models.FloatField(null=True, blank=True)
    pay_head = models.ForeignKey(Account)
    group_payroll = models.ForeignKey(GroupPayroll, related_name='rows')


class IndividualPayroll(models.Model):
    employee = models.ForeignKey(Employee)
    voucher_no = models.CharField(max_length=50)
    date = models.DateField()
    company = models.ForeignKey(Company)
    #days_worked = models.FloatField()
    #hours_worked = models.FloatField()
    #ot_hours_worked = models.FloatField()
    day_rate = models.FloatField(null=True, blank=True)
    hour_rate = models.FloatField(null=True, blank=True)
    ot_hour_rate = models.FloatField(null=True, blank=True)
    statuses = [('Approved', 'Approved'), ('Unapproved', 'Unapproved')]
    status = models.CharField(max_length=10, choices=statuses, default='Unapproved')


class Inclusion(models.Model):
    particular = models.ForeignKey(Account)
    amount = models.FloatField()
    individual_payroll = models.ForeignKey(IndividualPayroll, related_name='inclusions')


class Deduction(models.Model):
    particular = models.ForeignKey(Account)
    amount = models.FloatField()
    individual_payroll = models.ForeignKey(IndividualPayroll, related_name='deductions')