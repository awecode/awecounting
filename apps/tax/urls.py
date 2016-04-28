from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views, api

web_urls = [
    url(r'^schemes/$', views.TaxSchemeList.as_view(), name='tax_scheme_list'),
    url(r'^scheme/add/$', views.TaxSchemeCreate.as_view(), name='tax_scheme_add'),
    url(r'^scheme/edit/(?P<pk>\d+)/$', views.TaxSchemeUpdate.as_view(), name='tax_scheme_edit'),
    url(r'^scheme/delete/(?P<pk>\d+)/$', views.TaxSchemeDelete.as_view(), name='tax_scheme_delete'),
]

api_urls = [
    url(r'^api/tax_schemes/$', api.TaxSchemeListAPI.as_view()),
    url(r'^api/tax_scheme/(?P<pk>[0-9]+)/$', api.TaxSchemeDetailAPI.as_view()),
]

api_urls = format_suffix_patterns(api_urls)

urlpatterns = web_urls + api_urls
