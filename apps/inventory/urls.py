from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

import views
import api

urlpatterns = [
    url(r'^item/add/$', views.item, name='item_add'),
    url(r'^item/$', views.ItemList.as_view(), name='item_list'),
    url(r'^item/(?P<pk>[0-9]+)/$', views.item, name='item_edit'),
    url(r'^item/search/$', views.item_search, name='search-item'),
    url(r'^item/delete/(?P<pk>\d+)/$', views.ItemDelete.as_view(), name='item_delete'),

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

    

    # rest_framework api
    url(r'^api/items/$', api.ItemListAPI.as_view()),
    
    url(r'^api/units/$', api.UnitListAPI.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
