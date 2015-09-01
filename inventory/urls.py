from django.conf.urls import patterns, url
import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
                       url(r'^item/add/$', views.item, name='add-item'),
                       url(r'^item/$', views.item_list, name='item-list'),
                       url(r'^item/detail/(?P<id>[0-9]+)/$', views.item, name='item-detail'),

                       url(r'^party/add$', views.party_form, name='add-party'),
                       url(r'^party/$', views.parties_list, name='list_parties'),
                       url(r'^party/detail/(?P<id>[0-9]+)/$', views.party_form, name='party-detail'),

                       url(r'^unit/add$', views.unit_form, name='add-unit'),
                       url(r'^unit/$', views.unit_list, name='list_units'),
                       url(r'^unit/detail/(?P<id>[0-9]+)/$', views.unit_form, name='unit-detail'),

                       url(r'^accounts/$', views.list_inventory_accounts, name='list_inventory_accounts'),
                       url(r'^account/(?P<id>[0-9]+)/$', views.view_inventory_account, name='view_inventory_account'),


                       url(r'^purchase/create/$', views.purchase, name='purchase-create'),
                       url(r'^save/purchase/$', views.save_purchase, name='purchase-save'),
                       url(r'^purchase/list/$', views.purchase_list, name='purchase-list'),
                       url(r'^purchase/detail/(?P<id>[0-9]+)/$', views.purchase, name='purchase-detail'),

                       url(r'^sale/create/$', views.sale, name='sale-create'),
                       url(r'^save/sale/$', views.save_sale, name='sale-save'),
                       url(r'^sale/list/$', views.sale_list, name='sale-list'),
                       url(r'^sale/detail/(?P<id>[0-9]+)/$', views.sale, name='sale-detail'),

                       # rest_framework api
                       url(r'^api/items/$', views.ItemList.as_view()),
                       url(r'^api/parties/$', views.PartyList.as_view()),
                       url(r'^api/units/$', views.UnitList.as_view()),


)

urlpatterns = format_suffix_patterns(urlpatterns)