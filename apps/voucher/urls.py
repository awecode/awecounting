from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

import views
import api

web_urls = [
    url(r'^purchase/create/$', views.PurchaseVoucherCreate.as_view(), name='purchase-create'),
    url(r'^purchase/save/$', views.save_purchase, name='purchase-save'),
    url(r'^purchase/list/$', views.PurchaseVoucherList.as_view(), name='purchase-list'),
    url(r'^purchase/(?P<pk>[0-9]+)/$', views.PurchaseVoucherCreate.as_view(), name='purchase-edit'),
    url(r'^purchase/detail/(?P<pk>[0-9]+)/$', views.PurchaseVoucherDetailView.as_view(), name='purchase-detail'),
    url(r'^purchase/delete/(?P<pk>[0-9]+)$', views.PurchaseVoucherDelete.as_view(), name='purchase_delete'),

    url(r'^purchase_order/create/$', views.PurchaseOrderCreate.as_view(), name='purchase_order_create'),
    url(r'^purchase_order/save/$', views.save_purchase_order, name='purchase_order_save'),
    url(r'^purchase_order/list/$', views.PurchaseOrderList.as_view(), name='purchase_order_list'),
    url(r'^purchase_order/(?P<pk>[0-9]+)/$', views.PurchaseOrderCreate.as_view(), name='purchase_order_edit'),
    url(r'^purchase_order/detail/(?P<pk>[0-9]+)/$', views.PurchaseOrderDetailView.as_view(), name='purchase_order_detail'),
    url(r'^purchase_order/delete/(?P<pk>[0-9]+)$', views.PurchaseOrderDelete.as_view(), name='purchase_order_delete'),
    url(r'^incoming/purchase_order/$', views.IncomingPurchaseOrder.as_view(), name='incoming_purchase_order'),


    url(r'^sale/$', views.SaleCreate.as_view(), name='sale-create'),
    url(r'^sale/save/$', views.save_sale, name='sale-save'),
    url(r'^sale/list/$', views.SaleList.as_view(), name='sale-list'),
    url(r'^sale/(?P<pk>[0-9]+)/$', views.SaleCreate.as_view(), name='sale-edit'),
    url(r'^sale/(?P<voucher_date>\d{4}-\d{2}-\d{2})/$', views.sale_day, name='sale-day'),
    url(r'^sale/(?P<from_date>\d{4}-\d{2}-\d{2})/(?P<to_date>\d{4}-\d{2}-\d{2})/$', views.sale_date_range,
        name='sale-date-range'),
    url(r'^sale/report/$', views.sales_report_router, name='sale-report-router'),
    url(r'^sale/today/$', views.daily_sale_today, name='today_sale'),
    url(r'^sale/yesterday/$', views.daily_sale_yesterday, name='yesterday_sale'),
    url(r'^sale/detail/(?P<pk>[0-9]+)/$', views.SaleDetailView.as_view(), name='sale_detail'),

    url(r'^journal/$', views.JournalVoucherList.as_view(), name='journal_voucher_list'),
    url(r'^journal/add/$', views.JournalVoucherCreate.as_view(), name='journal_voucher_add'),
    url(r'^journal/(?P<pk>[0-9]+)/$', views.JournalVoucherCreate.as_view(), name='journal_voucher_edit'),
    url(r'^journal/save/$', views.journal_voucher_save, name='journal_voucher_save'),
    url(r'^journal/detail/(?P<pk>[0-9]+)/$', views.JournalVoucherDetailView.as_view(), name='journal_detail'),

    url(r'^cash_receipt/list/$', views.CashReceiptList.as_view(), name='cash_receipt_list'),
    url(r'^cash_receipt/create/$', views.CashReceiptCreate.as_view(), name='cash_receipt_add'),
    url(r'^cash_receipt/(?P<pk>[0-9]+)/$', views.CashReceiptCreate.as_view(), name='cash_receipt_edit'),
    url(r'^cash-receipt/save/$', views.save_cash_receipt, name='cash_receipt_save'),
    url(r'^cash_receipt/detail/(?P<pk>[0-9]+)/$', views.CashReceiptDetailView.as_view(), name='cash_receipt_detail'),

    url(r'^cash_payment/list/$', views.CashPaymentList.as_view(), name='cash_payment_list'),
    url(r'^cash_payment/create/$', views.CashPaymentCreate.as_view(), name='cash_payment_add'),
    url(r'^cash_payment/(?P<pk>[0-9]+)/$', views.CashPaymentCreate.as_view(), name='cash_payment_edit'),
    url(r'^cash_payment/save/$', views.save_cash_payment, name='cash_payment_save'),
    url(r'^cash_payment/detail/(?P<pk>[0-9]+)/$', views.CashPaymentDetailView.as_view(), name='cash_payment_detail'),

    url(r'^fixed_asset/$', views.FixedAssetList.as_view(), name='fixed_asset_list'),
    url(r'^fixed_asset/add/$', views.FixedAssetCreate.as_view(), name='fixed_asset_add'),
    url(r'^fixed_asset/(?P<pk>[0-9]+)/$', views.FixedAssetCreate.as_view(), name='fixed_asset_edit'),
    url(r'^fixed_asset/save/$', views.save_fixed_asset, name='fixed_asset_save'),
    url(r'^fixed_asset/delete/(?P<pk>[0-9]+)$', views.FixedAssetDelete.as_view(), name='fixed_asset_delete'),
    url(r'^fixed_asset/detail/(?P<pk>[0-9]+)/$', views.FixedAssetDetailView.as_view(), name='fixed_asset_detail'),


]

api_urls = [
    url(r'^api/sale/(?P<party_pk>[0-9]+)/(?P<receipt_pk>[0-9]+)$', api.PendingSaleListAPI.as_view()),
    url(r'^api/purchase/(?P<party_pk>[0-9]+)/(?P<payment_pk>[0-9]+)$', api.PendingPurchaseListAPI.as_view()),
    url(r'^api/cash_payments/', api.CashPaymentListAPI.as_view()),
    url(r'^api/cash_payment/(?P<pk>[0-9]+)/', api.CashPaymentDetailAPI.as_view()),
    url(r'^api/cash_receipts/', api.CashReceiptListAPI.as_view()),
    url(r'^api/cash_receipt/(?P<pk>[0-9]+)/', api.CashReceiptDetailAPI.as_view()),
    url(r'^api/fixed_assets/', api.FixedAssetListAPI.as_view()),
    url(r'^api/fixed_asset/(?P<pk>[0-9]+)/', api.FixedAssetDetailAPI.as_view()),
]

api_urls = format_suffix_patterns(api_urls)

urlpatterns = web_urls + api_urls
