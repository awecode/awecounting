from django.conf.urls import url
from . import views, api
from rest_framework.urlpatterns import format_suffix_patterns


web_urls = [
    url(r'^shareholder/$', views.ShareHolderList.as_view(), name='shareholder_list'),
    url(r'^shareholder/add/$', views.ShareHolderCreate.as_view(), name='shareholder_add'),
    url(r'^shareholder/edit/(?P<pk>\d+)/$', views.ShareHolderUpdate.as_view(), name='shareholder_edit'),
    url(r'^shareholder/delete/(?P<pk>\d+)/$', views.ShareHolderDelete.as_view(), name='shareholder_delete'),

    url(r'^collection/$', views.CollectionList.as_view(), name='collection_list'),
    url(r'^collection/add/$', views.CollectionCreate.as_view(), name='collection_add'),
    url(r'^collection/edit/(?P<pk>\d+)/$', views.CollectionUpdate.as_view(), name='collection_edit'),
    url(r'^collection/delete/(?P<pk>\d+)/$', views.CollectionDelete.as_view(), name='collection_delete'),

    url(r'^investment/$', views.InvestmentList.as_view(), name='investment_list'),
    url(r'^investment/add/$', views.InvestmentCreate.as_view(), name='investment_add'),
    url(r'^investment/edit/(?P<pk>\d+)/$', views.InvestmentUpdate.as_view(), name='investment_edit'),
    url(r'^investment/delete/(?P<pk>\d+)/$', views.InvestmentDelete.as_view(), name='investment_delete'),

]

api_urls = [
    url(r'^api/shareholders/$', api.ShareHolderListAPI.as_view()),
    url(r'^api/shareholder/(?P<pk>[0-9]+)/$', api.ShareHolderDetailAPI.as_view()),
    url(r'^api/collections/$', api.CollectionListAPI.as_view()),
    url(r'^api/collection/(?P<pk>[0-9]+)/$', api.CollectionDetailAPI.as_view()),
    url(r'^api/investments/$', api.InvestmentListAPI.as_view()),
    url(r'^api/investment/(?P<pk>[0-9]+)/$', api.InvestmentDetailAPI.as_view()),

]

api_urls = format_suffix_patterns(api_urls)

urlpatterns = web_urls + api_urls
