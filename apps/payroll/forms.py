from django import forms
from awecounting.utils.forms import HTML5BootstrapModelForm
from .models import Employee, AttendanceVoucher


class EmployeeForm(HTML5BootstrapModelForm):
    class Meta:
        model = Employee
        exclude = ['account', 'company']


class AttendanceVoucherForm(HTML5BootstrapModelForm):
    class Meta:
        model = AttendanceVoucher
        exclude = ['company',]