from django.contrib import admin
from inventory.models import Unit, Item, Purchase, PurchaseRow, Party, Sale, SaleRow, InventoryAccount, Transaction, JournalEntry, UnitConverter
from modeltranslation.admin import TranslationAdmin

class PurchaseRowInline(admin.TabularInline):
	model = PurchaseRow

class PurchaseAdmin(admin.ModelAdmin):
	inlines = [
		PurchaseRowInline,
	]

class SaleRowInline(admin.TabularInline):
	model = SaleRow

class SaleAdmin(admin.ModelAdmin):
	inlines = [
		SaleRowInline,
	]

admin.site.register(Unit, TranslationAdmin)
admin.site.register(Item, TranslationAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(PurchaseRow)
admin.site.register(Party, TranslationAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(SaleRow)
admin.site.register(InventoryAccount)
admin.site.register(Transaction)
admin.site.register(JournalEntry)
admin.site.register(UnitConverter)




