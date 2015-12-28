from django.contrib import admin
from .models import BankAccount, BankCashDeposit, ChequeDeposit, ChequeDepositRow


class ChequeDepositRowInline(admin.TabularInline):
    model = ChequeDepositRow


class ChequeDepositAdmin(admin.ModelAdmin):
    inlines = [
        ChequeDepositRowInline,
    ]

admin.site.register(BankAccount)
admin.site.register(BankCashDeposit)
admin.site.register(ChequeDeposit, ChequeDepositAdmin)

# Register your models here.
