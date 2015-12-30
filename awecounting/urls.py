"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from apps.inventory import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='home'),
    url(r'^users/', include('apps.users.urls', namespace='users')),
    url(r'^share/', include('apps.share.urls', namespace='share')),
    # url(r'^account/', include('apps.account.urls', namespace='account')),

    url(r'^inventory/', include('apps.inventory.urls')),
    url(r'^ledger/', include('apps.ledger.urls')),
    url(r'^bank/', include('apps.bank.urls', namespace='bank')),
    url(r'^njango/', include('njango.urls')),

]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT})
        ]
