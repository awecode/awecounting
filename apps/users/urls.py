from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
                       url(r'^$', views.UserListView.as_view(), name='user_list'),
                       url(r'^login/$', views.web_login, name='login'),
                       url(r'^logout/$', views.logout, name='logout'),
                       url(r'^add/$', views.UserCreate.as_view(), name='user_add'),
                       url(r'^edit/(?P<pk>\d+)/$', views.UserUpdate.as_view(), name='user_edit'),
                       url(r'^delete/(?P<pk>\d+)/$', views.UserDelete.as_view(), name='user_delete'),

                       # url(r'^groups/$', views.GroupListView.as_view(), name='group_list'),
                       # url(r'^groups/add/$', views.GroupCreateView.as_view(), name='group_add'),
                       # url(r'^groups/edit/(?P<pk>\d+)$', views.GroupUpdateView.as_view(), name='group_edit'),
                       # url(r'^groups/delete/(?P<pk>\d+)$', views.GroupDeleteView.as_view(), name='group_delete'),

                       url(r'^set-role/(?P<pk>[0-9]+)/$', views.set_role, name='set_role'),
                       url(r'^roles/$', views.roles, name='roles'),
                       url(r'^role/delete/(?P<pk>[0-9]+)/$', views.delete_role, name='delete_role'),
                       url(r'^role/(?P<pk>\d+)/$', views.RoleUpdate.as_view(), name='edit_role'),
                       )
