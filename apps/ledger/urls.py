from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views
import api

web_urls = [
    url(r'^$', views.AccountList.as_view(), name='list_account'),
    url(r'^(?P<pk>[0-9]+)/$', views.ViewAccount.as_view(), name='view_ledger'),
    url(r'^item/(?P<pk>[0-9]+)/$', views.ViewItemAccount.as_view(), name='ledger'),

    url(r'^party/$', views.PartyList.as_view(), name='party_list'),
    url(r'^party/add/$', views.PartyCreate.as_view(), name='party_add'),
    url(r'^party/edit/(?P<pk>\d+)/$', views.PartyUpdate.as_view(), name='party_edit'),
    url(r'^party/delete/(?P<pk>\d+)/$', views.PartyDelete.as_view(), name='party_delete'),

    url(r'^categories/$', views.CategoryList.as_view(), name='category_list'),
    url(r'^category/add/$', views.CategoryCreate.as_view(), name='category_add'),
    url(r'^category/edit/(?P<pk>\d+)/$', views.CategoryUpdate.as_view(), name='category_edit'),
    url(r'^category/delete/(?P<pk>\d+)/$', views.CategoryDelete.as_view(), name='category_delete'),

    url(r'^accounts/$', views.AccountList.as_view(), name='account_list'),
    url(r'^accounts/tree/$', views.AccountTree.as_view(), name='account_tree'),
    url(r'^account/add/$', views.AccountCreate.as_view(), name='account_add'),
    url(r'^account/edit/(?P<pk>\d+)/$', views.AccountUpdate.as_view(), name='account_edit'),
    url(r'^account/delete/(?P<pk>\d+)/$', views.AccountDelete.as_view(), name='account_delete'),
]

api_urls = [
    url(r'^api/account/$', api.AccountListAPI.as_view()),
    url(r'^api/parties/$', api.PartyListAPI.as_view()),
    url(r'^api/parties_with_balance/$', api.PartyBalanceListAPI.as_view()),
    url(r'^api/(?P<category>.+)/account/$', api.AccountListAPI.as_view()),
    url(r'^api/bank_cash_account/$', api.BankAndCashAccountListAPI.as_view()),
    url(r'^api/categories/$', api.CategoryListAPI.as_view()),
    url(r'^api/category/(?P<pk>[0-9]+)/$', api.CategoryDetailAPI.as_view()),
]

api_urls = format_suffix_patterns(api_urls)

urlpatterns = web_urls + api_urls
