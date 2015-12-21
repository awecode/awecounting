from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
                       url(r'^journalvoucher/$', views.JournalVoucherList.as_view(), name='journalvoucher_list'),
                       url(r'^journalvoucher/add/$', views.journalvoucher_create, name='journalvoucher_add'),
                       url(r'^journalvoucher/(?P<id>[0-9]+)/$', views.journalvoucher_create, name='journalvoucher_edit'),
                       url(r'^save/journal_voucher/$', views.journalvoucher_save, name='journalvoucher_save'),

                       # url(r'^journalvoucher/add/$', views.JournalVoucherCreate.as_view(), name='journalvoucher_add'),
                       # url(r'^shareholder/edit/(?P<pk>\d+)/$', views.ShareHolderUpdate.as_view(), name='shareholder_edit'),
                       # url(r'^shareholder/delete/(?P<pk>\d+)/$', views.ShareHolderDelete.as_view(), name='shareholder_delete'),
                       )
