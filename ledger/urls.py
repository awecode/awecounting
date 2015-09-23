from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^$', views.list_accounts, name='list_account'),
                       url(r'^(?P<id>[0-9]+)/$', views.view_account, name='view_account'),
)
