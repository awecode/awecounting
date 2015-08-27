from django.contrib import admin
from inventory.models import Unit, Item, Purchase, PurchaseRow, Party
from modeltranslation.admin import TranslationAdmin

admin.site.register(Unit, TranslationAdmin)
admin.site.register(Item, TranslationAdmin)
admin.site.register(Purchase)
admin.site.register(PurchaseRow)
admin.site.register(Party, TranslationAdmin)

