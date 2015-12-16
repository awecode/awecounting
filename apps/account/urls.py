from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
                       url(r'^journalvoucher/$', views.JournalVoucherList.as_view(), name='journalvoucher_list'),
                       # url(r'^shareholder/add/$', views.ShareHolderCreate.as_view(), name='shareholder_add'),
                       # url(r'^shareholder/edit/(?P<pk>\d+)/$', views.ShareHolderUpdate.as_view(), name='shareholder_edit'),
                       # url(r'^shareholder/delete/(?P<pk>\d+)/$', views.ShareHolderDelete.as_view(), name='shareholder_delete'),
                       )
