from django.contrib import admin
from .models import JournalVoucher, JournalVoucherRow

class JournalVoucherRowInline(admin.TabularInline):
	model = JournalVoucherRow


class JournalVoucherAdmin(admin.ModelAdmin):
	inlines = [
		JournalVoucherRowInline,
	]

admin.site.register(JournalVoucher, JournalVoucherAdmin)
admin.site.register(JournalVoucherRow)
# Register your models here.
