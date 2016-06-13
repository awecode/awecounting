from django.contrib import admin

from awecounting.utils.mixins import CompanyAdmin
from .models import FixedAsset, FixedAssetRow, AdditionalDetail, PurchaseVoucherRow, SaleRow, PurchaseVoucher, Sale, \
    JournalVoucher, \
    JournalVoucherRow, CashReceipt, CashReceiptRow, CashPayment, CashPaymentRow, PurchaseOrder, PurchaseOrderRow, VoucherSetting, \
    ExpenseRow, Expense, TradeExpense, Lot, LotItemDetail, SaleFromLocation


class PurchaseVoucherRowInline(admin.TabularInline):
    model = PurchaseVoucherRow


class PurchaseVoucherAdmin(CompanyAdmin):
    inlines = [
        PurchaseVoucherRowInline,
    ]


class ExpenseRowInline(admin.TabularInline):
    model = ExpenseRow


class ExpenseAdmin(CompanyAdmin):
    inlines = [
        ExpenseRowInline,
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


class VoucherSettingStacked(admin.StackedInline):
    model = VoucherSetting


admin.site.register(PurchaseVoucher, PurchaseVoucherAdmin)
admin.site.register(PurchaseVoucherRow)
admin.site.register(Sale, SaleAdmin)
admin.site.register(SaleRow)
admin.site.register(FixedAsset, FixedAssetAdmin)
admin.site.register(FixedAssetRow)
admin.site.register(AdditionalDetail)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(PurchaseOrderRow, PurchaseOrderRowAdmin)
admin.site.register(VoucherSetting, CompanyAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(ExpenseRow)
admin.site.register(TradeExpense)


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
admin.site.register(Lot)
admin.site.register(LotItemDetail)
admin.site.register(SaleFromLocation)


