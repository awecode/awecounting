from django.conf.urls import patterns, url
import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
                       url(r'^item/add/$', views.item, name='add-item'),

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