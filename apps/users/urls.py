from django.conf.urls import patterns, url
from . import views, api
from rest_framework.urlpatterns import format_suffix_patterns


web_urls = [
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
    url(r'^send_pin/', views.AddUserPin.as_view(), name="add_user_with_pin"),
    url(r'^company_setting/$', views.CompanySettingUpdateView.as_view(), name='company_setting'),
    url(r'^api/pin/(?P<pin>\d+-\d+)/$', views.ValidatePin.as_view(), name='validate_pin'),

    url(r'^company_pin/', views.CompanyPin.as_view(), name="company_pin"),
    url(r'^accessible_company_list/', views.AccessibleCompanies.as_view(), name="accessible_company_list"),

    url(r'^set_company_to_party/(?P<company_id>\d+)/$', views.set_company_to_party, name='set_company_to_party'),
    url(r'^party_for_company/(?P<company_id>\d+)/$', views.party_for_company, name='party_for_company'),
]

api_urls = [
    url(r'^api/asseccible_company/$', api.AccessibleCompanyAPI.as_view()),
]

api_urls = format_suffix_patterns(api_urls)

urlpatterns = web_urls + api_urls

