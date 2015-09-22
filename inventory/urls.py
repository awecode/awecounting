from django.conf.urls import patterns, url
import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
                       url(r'^item/add/$', views.item, name='add-item'),
                       url(r'^item/$', views.item_list, name='item-list'),
                       url(r'^item/(?P<id>[0-9]+)/$', views.item, name='item-detail'),
                       url(r'^item/search/$', views.item_search, name='search-item'),

                       url(r'^party/add$', views.party_form, name='add-party'),
                       url(r'^party/$', views.parties_list, name='list_parties'),
                       url(r'^party/(?P<id>[0-9]+)/$', views.party_form, name='party-detail'),

                       url(r'^unit/add$', views.unit_form, name='add-unit'),
                       url(r'^unit/$', views.unit_list, name='list_units'),
                       url(r'^unit/(?P<id>[0-9]+)/$', views.unit_form, name='unit-detail'),

                       url(r'^accounts/$', views.list_inventory_accounts, name='list_inventory_accounts'),
                       url(r'^accounts/(?P<id>[0-9]+)/$', views.view_inventory_account, name='view_inventory_account'),
                       url(r'^accounts/(?P<id>[0-9]+)/rate/$', views.view_inventory_account_with_rate,
                           name='view_inventory_account_with_rate'),

                       url(r'^purchase/create/$', views.purchase, name='purchase-create'),
                       url(r'^save/purchase/$', views.save_purchase, name='purchase-save'),
                       url(r'^purchase/list/$', views.purchase_list, name='purchase-list'),
                       url(r'^purchase/(?P<id>[0-9]+)/$', views.purchase, name='purchase-detail'),

                       url(r'^sale/create/$', views.sale, name='sale-create'),
                       url(r'^save/sale/$', views.save_sale, name='sale-save'),
                       url(r'^sale/list/$', views.sale_list, name='sale-list'),
                       url(r'^sale/(?P<id>[0-9]+)/$', views.sale, name='sale-detail'),
                       url(r'^sale/(?P<voucher_date>\d{4}-\d{2}-\d{2})/$', views.sale_day, name='sale-day'),
                       url(r'^sale/(?P<from_date>\d{4}-\d{2}-\d{2})/(?P<to_date>\d{4}-\d{2}-\d{2})/$', views.sale_date_range,
                           name='sale-date-range'),

                       url(r'^daily-sale/today$', views.daily_sale_today, name='today_sale'),
                       url(r'^daily-sale/yesterday$', views.daily_sale_yesterday, name='yesterday_sale'),

                       # rest_framework api
                       url(r'^api/items/$', views.ItemList.as_view()),
                       url(r'^api/parties/$', views.PartyList.as_view()),
                       url(r'^api/units/$', views.UnitList.as_view()),

                       )

urlpatterns = format_suffix_patterns(urlpatterns)
