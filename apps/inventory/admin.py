from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from awecounting.utils.mixins import TranslationCompanyAdmin, CompanyAdmin

from .models import Unit, Item, InventoryAccount, Transaction, JournalEntry, UnitConversion, Location, LocationContain, \
    ItemCategory

admin.site.register(Unit, TranslationCompanyAdmin)
admin.site.register(Item, CompanyAdmin)
admin.site.register(InventoryAccount, CompanyAdmin)
admin.site.register(Transaction)
admin.site.register(JournalEntry)
admin.site.register(Location)
admin.site.register(LocationContain)
admin.site.register(ItemCategory)
admin.site.register(UnitConversion, CompanyAdmin)
