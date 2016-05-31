from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from awecounting.utils.mixins import TranslationCompanyAdmin, CompanyAdmin

from .models import Unit, Item, InventoryAccount, Transaction, JournalEntry, UnitConversion

admin.site.register(Unit, TranslationCompanyAdmin)
admin.site.register(Item)
admin.site.register(InventoryAccount, CompanyAdmin)
admin.site.register(Transaction)
admin.site.register(JournalEntry)
admin.site.register(UnitConversion, CompanyAdmin)
