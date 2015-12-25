from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
                       url(r'^journal_voucher/$', views.JournalVoucherList.as_view(), name='journal_voucher_list'),
                       url(r'^journal_voucher/add/$', views.journal_voucher_create, name='journal_voucher_add'),
                       url(r'^journal_voucher/(?P<id>[0-9]+)/$', views.journal_voucher_create, name='journal_voucher_edit'),
                       url(r'^save/journal_voucher/$', views.journal_voucher_save, name='journal_voucher_save'),

                       # url(r'^journalvoucher/add/$', views.JournalVoucherCreate.as_view(), name='journalvoucher_add'),
                       # url(r'^shareholder/edit/(?P<pk>\d+)/$', views.ShareHolderUpdate.as_view(), name='shareholder_edit'),
                       # url(r'^shareholder/delete/(?P<pk>\d+)/$', views.ShareHolderDelete.as_view(), name='shareholder_delete'),
                       )
