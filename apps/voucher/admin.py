from django.contrib import admin
from .models import PurchaseRow, SaleRow, Purchase, Sale, JournalVoucher, JournalVoucherRow


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


admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(PurchaseRow)
admin.site.register(Sale, SaleAdmin)
admin.site.register(SaleRow)


class JournalVoucherRowInline(admin.TabularInline):
    model = JournalVoucherRow


class JournalVoucherAdmin(admin.ModelAdmin):
    inlines = [
        JournalVoucherRowInline,
    ]


admin.site.register(JournalVoucher, JournalVoucherAdmin)
admin.site.register(JournalVoucherRow)
