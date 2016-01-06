from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Account, Transaction, JournalEntry, Party


class AccountAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'current_cr', 'current_dr', 'parent', 'category']
    list_filter = ['company']
    list_display_links = ['code', 'name']


admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction)
admin.site.register(JournalEntry)
admin.site.register(Party, TranslationAdmin)
