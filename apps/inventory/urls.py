from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from apps.inventory import views

urlpatterns = patterns('',
                       url(r'^item/add/$', views.item, name='item_add'),
                       url(r'^item/$', views.ItemList.as_view(), name='item_list'),
                       url(r'^item/(?P<id>[0-9]+)/$', views.item, name='item_edit'),
                       url(r'^item/search/$', views.item_search, name='search-item'),
                       url(r'^item/delete/(?P<pk>\d+)/$', views.ItemDelete.as_view(), name='item_delete'),


                       url(r'^party/$', views.PartyList.as_view(), name='parties_list'),
                       url(r'^party/add/$', views.PartyCreate.as_view(), name='party_add'),
                       url(r'^party/edit/(?P<pk>\d+)/$', views.PartyUpdate.as_view(), name='party_edit'),
                       url(r'^party/delete/(?P<pk>\d+)/$', views.PartyDelete.as_view(), name='party_delete'),

                       url(r'^unit/add$', views.UnitCreate.as_view(), name='unit_add'),
                       url(r'^unit/$', views.UnitList.as_view(), name='unit_list'),
                       url(r'^unit/edit/(?P<pk>\d+)/$', views.UnitUpdate.as_view(), name='unit_edit'),
                       url(r'^unit/delete/(?P<pk>\d+)/$', views.UnitDelete.as_view(), name='unit_delete'),

                       url(r'^unitconverter/$', views.UnitConverterList.as_view(), name='unitconverter_list'),
                       url(r'^unitconverter/add/$', views.UnitConverterCreate.as_view(), name='unitconverter_add'),
                       url(r'^unitconverter/edit/(?P<pk>\d+)/$', views.UnitConverterUpdate.as_view(), name='unitconverter_edit'),
                       url(r'^unitconverter/delete/(?P<pk>\d+)/$', views.UnitConverterDelete.as_view(), name='unitconverter_delete'),


                       url(r'^accounts/$', views.list_inventory_accounts, name='list_inventory_accounts'),
                       url(r'^accounts/(?P<id>[0-9]+)/$', views.view_inventory_account, name='view_inventory_account'),
                       url(r'^accounts/(?P<id>[0-9]+)/rate/$', views.view_inventory_account_with_rate,
                           name='view_inventory_account_with_rate'),

                       url(r'^purchase/create/$', views.purchase, name='purchase-create'),
                       url(r'^save/purchase/$', views.save_purchase, name='purchase-save'),
                       url(r'^purchase/list/$', views.purchase_list, name='purchase-list'),
                       url(r'^purchase/(?P<id>[0-9]+)/$', views.purchase, name='purchase-detail'),

                       url(r'^sale/$', views.sale, name='sale-create'),
                       url(r'^save/sale/$', views.save_sale, name='sale-save'),
                       url(r'^sale/list/$', views.sale_list, name='sale-list'),
                       url(r'^sale/(?P<id>[0-9]+)/$', views.sale, name='sale-detail'),
                       url(r'^sale/(?P<voucher_date>\d{4}-\d{2}-\d{2})/$', views.sale_day, name='sale-day'),
                       url(r'^sale/(?P<from_date>\d{4}-\d{2}-\d{2})/(?P<to_date>\d{4}-\d{2}-\d{2})/$', views.sale_date_range,
                           name='sale-date-range'),
                       url(r'^sale/report/$', views.sales_report_router, name='sale-report-router'),
                       url(r'^sale/today/$', views.daily_sale_today, name='today_sale'),
                       url(r'^sale/yesterday/$', views.daily_sale_yesterday, name='yesterday_sale'),

                       # rest_framework api
                       url(r'^api/items/$', views.ItemListAPI.as_view()),
                       url(r'^api/parties/$', views.PartyListAPI.as_view()),
                       url(r'^api/units/$', views.UnitListAPI.as_view()),

                       )

urlpatterns = format_suffix_patterns(urlpatterns)
