from django.contrib import admin
from .models import BankAccount, BankCashDeposit

admin.site.register(BankAccount)
admin.site.register(BankCashDeposit)

# Register your models here.
