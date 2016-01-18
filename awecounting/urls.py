from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^$', 'apps.inventory.views.index', name='home'),

    url(r'^users/', include('apps.users.urls', namespace='users')),
    url(r'^share/', include('apps.share.urls', namespace='share')),
    url(r'^inventory/', include('apps.inventory.urls')),
    url(r'^ledger/', include('apps.ledger.urls')),
    url(r'^voucher/', include('apps.voucher.urls')),
    url(r'^bank/', include('apps.bank.urls', namespace='bank')),
    url(r'^njango/', include('njango.urls')),

]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT})
    ]
