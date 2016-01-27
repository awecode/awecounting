from django import forms
from apps.payroll.models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['account', 'company']