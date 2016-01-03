from django.conf.urls import url

import views
import api

urlpatterns = [

    url(r'^purchase/create/$', views.purchase, name='purchase-create'),
    url(r'^purchase/save/$', views.save_purchase, name='purchase-save'),
    url(r'^purchase/list/$', views.purchase_list, name='purchase-list'),
    url(r'^purchase/(?P<id>[0-9]+)/$', views.purchase, name='purchase-detail'),

    url(r'^sale/$', views.sale, name='sale-create'),
    url(r'^sale/save/$', views.save_sale, name='sale-save'),
    url(r'^sale/list/$', views.sale_list, name='sale-list'),
    url(r'^sale/(?P<id>[0-9]+)/$', views.sale, name='sale-detail'),
    url(r'^sale/(?P<voucher_date>\d{4}-\d{2}-\d{2})/$', views.sale_day, name='sale-day'),
    url(r'^sale/(?P<from_date>\d{4}-\d{2}-\d{2})/(?P<to_date>\d{4}-\d{2}-\d{2})/$', views.sale_date_range,
        name='sale-date-range'),
    url(r'^sale/report/$', views.sales_report_router, name='sale-report-router'),
    url(r'^sale/today/$', views.daily_sale_today, name='today_sale'),
    url(r'^sale/yesterday/$', views.daily_sale_yesterday, name='yesterday_sale'),

    url(r'^journal/$', views.JournalVoucherList.as_view(), name='journal_voucher_list'),
    url(r'^journal/add/$', views.journal_voucher_create, name='journal_voucher_add'),
    url(r'^journal/(?P<id>[0-9]+)/$', views.journal_voucher_create, name='journal_voucher_edit'),
    url(r'^journal/save/$', views.journal_voucher_save, name='journal_voucher_save'),

    url(r'^cash_receipt/$', views.cash_receipt, name='create_cash_receipt'),

    url(r'^api/sale/(?P<party_pk>[0-9]+)/$', api.PendingSaleListAPI.as_view()),
]
