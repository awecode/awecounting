from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

import views

urlpatterns = [
    url(r'^entry/create/$', views.EntryCreate.as_view(), name='entry_add'),
    url(r'^entry/save/$', views.save_entry, name='entry_save'),
    url(r'^entry/list/$', views.EntryList.as_view(), name='entry_list'),
    url(r'^entry/(?P<pk>[0-9]+)/$', views.EntryCreate.as_view(), name='entry_edit'),
    url(r'^entry/detail/(?P<pk>[0-9]+)/$', views.EntryDetailView.as_view(), name='entry_detail'),
]
