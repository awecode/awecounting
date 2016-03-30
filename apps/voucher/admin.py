from django.contrib import admin
from awecounting.utils.mixins import CompanyAdmin
from .models import FixedAsset, FixedAssetRow, AdditionalDetail, PurchaseRow, SaleRow, Purchase, Sale, JournalVoucher, \
    JournalVoucherRow, CashReceipt, CashReceiptRow, CashPayment, CashPaymentRow, PurchaseOrder, PurchaseOrderRow


class PurchaseRowInline(admin.TabularInline):
    model = PurchaseRow


class PurchaseAdmin(CompanyAdmin):
    inlines = [
        PurchaseRowInline,
    ]


class FixedAssetRowInline(admin.TabularInline):
    model = FixedAssetRow


class AdditionalDetailInline(admin.TabularInline):
    model = AdditionalDetail


class FixedAssetAdmin(CompanyAdmin):
    inlines = [
        FixedAssetRowInline,
        AdditionalDetailInline,
    ]


class SaleRowInline(admin.TabularInline):
    model = SaleRow


class SaleAdmin(CompanyAdmin):
    inlines = [
        SaleRowInline,
    ]


class PurchaseOrderRowInline(admin.TabularInline):
    model = PurchaseOrderRow


class PurchaseOrderRowAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity', 'unit',
                    'rate', 
                    # 'vattable',
                    'remarks')
    search_fields = ('item',)


class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'party', 'date')
    inlines = [
        PurchaseOrderRowInline,
    ]

admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(PurchaseRow)
admin.site.register(Sale, SaleAdmin)
admin.site.register(SaleRow)
admin.site.register(FixedAsset, FixedAssetAdmin)
admin.site.register(FixedAssetRow)
admin.site.register(AdditionalDetail)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(PurchaseOrderRow, PurchaseOrderRowAdmin)



class JournalVoucherRowInline(admin.TabularInline):
    model = JournalVoucherRow


class JournalVoucherAdmin(CompanyAdmin):
    inlines = [
        JournalVoucherRowInline,
    ]


class CashReceiptRowInline(admin.TabularInline):
    model = CashReceiptRow


class CashReceiptAdmin(CompanyAdmin):
    inlines = [
        CashReceiptRowInline,
    ]


class CashPaymentRowInline(admin.TabularInline):
    model = CashPaymentRow


class CashPaymentAdmin(CompanyAdmin):
    inlines = [
        CashPaymentRowInline,
    ]


admin.site.register(JournalVoucher, JournalVoucherAdmin)
admin.site.register(JournalVoucherRow)
admin.site.register(CashReceipt, CashReceiptAdmin)
admin.site.register(CashReceiptRow)
admin.site.register(CashPayment, CashPaymentAdmin)
admin.site.register(CashPaymentRow)
