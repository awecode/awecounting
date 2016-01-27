from django import forms
from awecounting.utils.forms import HTML5BootstrapModelForm
from .models import Employee, AttendanceVoucher
from django.core.urlresolvers import reverse_lazy


class EmployeeForm(HTML5BootstrapModelForm):
    class Meta:
        model = Employee
        exclude = ['account', 'company']


class AttendanceVoucherForm(HTML5BootstrapModelForm):
    class Meta:
        model = AttendanceVoucher
        exclude = ['company',]
        widgets = {
            'employee': forms.Select(attrs={'class': 'selectize', 'data-url': reverse_lazy('employee_add')}),
        }
        company_filters = ('employee',)
