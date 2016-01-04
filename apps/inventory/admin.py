from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Unit, Item, InventoryAccount, Transaction, JournalEntry, UnitConverter

admin.site.register(Unit, TranslationAdmin)
admin.site.register(Item, TranslationAdmin)
admin.site.register(InventoryAccount)
admin.site.register(Transaction)
admin.site.register(JournalEntry)
admin.site.register(UnitConverter)
