from django.conf.urls import patterns, url

from apps.ledger import views

urlpatterns = [
    url(r'^$', views.list_accounts, name='list_account'),
    url(r'^(?P<id>[0-9]+)/$', views.view_account, name='view_account'),

    url(r'^journal_voucher/$', views.JournalVoucherList.as_view(), name='journal_voucher_list'),
    url(r'^journal_voucher/add/$', views.journal_voucher_create, name='journal_voucher_add'),
    url(r'^journal_voucher/(?P<id>[0-9]+)/$', views.journal_voucher_create, name='journal_voucher_edit'),
    url(r'^save/journal_voucher/$', views.journal_voucher_save, name='journal_voucher_save'),

    # rest_framework api
    url(r'^api/account/$', views.AccountListAPI.as_view()),

]
