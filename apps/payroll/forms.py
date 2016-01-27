from django import forms
from awecounting.utils.forms import HTML5BootstrapModelForm
from .models import Employee


class EmployeeForm(HTML5BootstrapModelForm):
    class Meta:
        model = Employee
        exclude = ['account', 'company']