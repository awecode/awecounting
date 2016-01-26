from django.contrib import admin

from awecounting.utils.mixins import CompanyAdmin, TranslationCompanyAdmin

from .models import Account, Transaction, JournalEntry, Party, Category


class AccountAdmin(CompanyAdmin):
    list_display = ['code', 'name', 'current_cr', 'current_dr', 'parent', 'category']
    list_display_links = ['code', 'name']


admin.site.register(Account, AccountAdmin)
admin.site.register(Category, CompanyAdmin)
admin.site.register(Transaction)
admin.site.register(JournalEntry)
admin.site.register(Party, TranslationCompanyAdmin)
