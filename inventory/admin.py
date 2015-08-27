from django.contrib import admin
from .models import Unit, Item, Purchase, PurchaseRow, Party

admin.site.register(Unit)
admin.site.register(Item)
admin.site.register(Purchase)
admin.site.register(PurchaseRow)
admin.site.register(Party)

