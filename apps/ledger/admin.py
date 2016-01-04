from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Account, Transaction, JournalEntry, Party

admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(JournalEntry)
admin.site.register(Party, TranslationAdmin)
