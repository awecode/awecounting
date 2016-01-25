from django.contrib import admin
from .models import BankAccount, BankCashDeposit, ChequeDeposit, ChequeDepositRow, ChequePayment


class ChequeFileInline(admin.TabularInline):
    model = ChequeDeposit.files.through


class ChequeDepositRowInline(admin.TabularInline):
    model = ChequeDepositRow


class ChequeDepositAdmin(admin.ModelAdmin):
    inlines = [
        ChequeDepositRowInline, ChequeFileInline
    ]
    exclude = ['files',]


admin.site.register(BankAccount)
admin.site.register(BankCashDeposit)
admin.site.register(ChequeDeposit, ChequeDepositAdmin)
admin.site.register(ChequePayment)


# Register your models here.
