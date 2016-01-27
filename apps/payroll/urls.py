from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

import views
import api

web_urls = [
    url(r'^entry/create/$', views.EntryCreate.as_view(), name='entry_add'),
    url(r'^entry/save/$', views.save_entry, name='entry_save'),
    url(r'^entry/list/$', views.EntryList.as_view(), name='entry_list'),
    url(r'^entry/(?P<pk>[0-9]+)/$', views.EntryCreate.as_view(), name='entry_edit'),
    url(r'^entry/detail/(?P<pk>[0-9]+)/$', views.EntryDetailView.as_view(), name='entry_detail'),

    url(r'^employee/$', views.EmployeeList.as_view(), name='employee_list'),
    url(r'^employee/add/$', views.EmployeeCreate.as_view(), name='employee_add'),
    url(r'^employee/edit/(?P<pk>\d+)/$', views.EmployeeUpdate.as_view(), name='employee_edit'),
    url(r'^employee/delete/(?P<pk>\d+)/$', views.EmployeeDelete.as_view(), name='employee_delete'),
]

api_urls = [
    url(r'^api/employee/$', api.EmployeeListAPI.as_view()),
]

api_urls = format_suffix_patterns(api_urls)

urlpatterns = web_urls + api_urls
