from django.conf.urls import patterns, url

from apps.ledger import views

urlpatterns = patterns('',
                       url(r'^$', views.list_accounts, name='list_account'),
                       url(r'^(?P<id>[0-9]+)/$', views.view_account, name='view_account'),

                       # rest_framework api
                       url(r'^api/account/$', views.AccountListAPI.as_view()),

)
