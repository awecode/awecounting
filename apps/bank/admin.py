from django.contrib import admin
from awecounting.utils.mixins import CompanyAdmin
from .models import BankAccount, BankCashDeposit, ChequeDeposit, ChequeDepositRow, ChequePayment


class ChequeFileInline(admin.TabularInline):
    model = ChequeDeposit.files.through


class ChequeDepositRowInline(admin.TabularInline):
    model = ChequeDepositRow


class ChequeDepositAdmin(CompanyAdmin):
    inlines = [
        ChequeDepositRowInline, ChequeFileInline
    ]
    exclude = ['files', ]


admin.site.register(BankAccount, CompanyAdmin)
admin.site.register(BankCashDeposit)
admin.site.register(ChequeDeposit, ChequeDepositAdmin)
admin.site.register(ChequePayment, CompanyAdmin)


# Register your models here.
