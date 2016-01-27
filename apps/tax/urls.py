from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^tax_scheme/$', views.TaxSchemeList.as_view(), name='tax_scheme_list'),
    url(r'^tax_scheme/add/$', views.TaxSchemeCreate.as_view(), name='tax_scheme_add'),
    url(r'^tax_scheme/edit/(?P<pk>\d+)/$', views.TaxSchemeUpdate.as_view(), name='tax_scheme_edit'),
    url(r'^tax_scheme/delete/(?P<pk>\d+)/$', views.TaxSchemeDelete.as_view(), name='tax_scheme_delete'),
]
