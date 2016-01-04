from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views
import api

urlpatterns = [
    url(r'^$', views.list_accounts, name='list_account'),
    url(r'^(?P<id>[0-9]+)/$', views.view_account, name='view_account'),

    url(r'^party/$', views.PartyList.as_view(), name='party_list'),
    url(r'^party/add/$', views.PartyCreate.as_view(), name='party_add'),
    url(r'^party/edit/(?P<pk>\d+)/$', views.PartyUpdate.as_view(), name='party_edit'),
    url(r'^party/delete/(?P<pk>\d+)/$', views.PartyDelete.as_view(), name='party_delete'),

    url(r'^api/account/$', api.AccountListAPI.as_view()),
    url(r'^api/parties/$', api.PartyListAPI.as_view()),
    url(r'^api/(?P<category>.+)/account/$', api.AccountListAPI.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
