from django.contrib import admin

from apps.ledger.models import Account, Transaction, JournalEntry, JournalVoucher, JournalVoucherRow

class JournalVoucherRowInline(admin.TabularInline):
	model = JournalVoucherRow


class JournalVoucherAdmin(admin.ModelAdmin):
	inlines = [
		JournalVoucherRowInline,
	]
	

admin.site.register(JournalVoucher, JournalVoucherAdmin)
admin.site.register(JournalVoucherRow)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(JournalEntry)