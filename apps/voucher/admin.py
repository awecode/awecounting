from django.contrib import admin
from .models import FixedAsset, FixedAssetRow, AdditionalDetail, PurchaseRow, SaleRow, Purchase, Sale, JournalVoucher, JournalVoucherRow, CashReceipt, CashReceiptRow, CashPayment, CashPaymentRow


class PurchaseRowInline(admin.TabularInline):
    model = PurchaseRow


class PurchaseAdmin(admin.ModelAdmin):
    inlines = [
        PurchaseRowInline,
    ]


class FixedAssetRowInline(admin.TabularInline):
    model = FixedAssetRow


class AdditionalDetailInline(admin.TabularInline):
    model = AdditionalDetail


class FixedAssetAdmin(admin.ModelAdmin):
    inlines = [
        FixedAssetRowInline,
        AdditionalDetailInline,
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
admin.site.register(FixedAsset, FixedAssetAdmin)
admin.site.register(FixedAssetRow)
admin.site.register(AdditionalDetail)


class JournalVoucherRowInline(admin.TabularInline):
    model = JournalVoucherRow


class JournalVoucherAdmin(admin.ModelAdmin):
    inlines = [
        JournalVoucherRowInline,
    ]


class CashReceiptRowInline(admin.TabularInline):
    model = CashReceiptRow


class CashReceiptAdmin(admin.ModelAdmin):
    inlines = [
        CashReceiptRowInline,
    ]


class CashPaymentRowInline(admin.TabularInline):
    model = CashPaymentRow


class CashPaymentAdmin(admin.ModelAdmin):
    inlines = [
        CashPaymentRowInline,
    ]

admin.site.register(JournalVoucher, JournalVoucherAdmin)
admin.site.register(JournalVoucherRow)
admin.site.register(CashReceipt, CashReceiptAdmin)
admin.site.register(CashReceiptRow)
admin.site.register(CashPayment, CashPaymentAdmin)
admin.site.register(CashPaymentRow)

