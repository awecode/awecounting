from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from rest_framework.authtoken import views
from django.conf.urls.static import static

from apps.inventory import views as inventory_views
from apps.users import views as users_views

urlpatterns = [
                  url(r'^admin/', include(admin.site.urls)),
                  url(r'^i18n/', include('django.conf.urls.i18n')),
                  url(r'^$', inventory_views.index, name='home'),
                  url(r'^test$', users_views.test, name='test'),
                  url(r'^demo/$', users_views.demo_login, name='demo'),

                  url(r'^users/', include('apps.users.urls', namespace='users')),
                  url(r'^share/', include('apps.share.urls', namespace='share')),
                  url(r'^tax/', include('apps.tax.urls')),
                  url(r'^payroll/', include('apps.payroll.urls')),
                  url(r'^inventory/', include('apps.inventory.urls')),
                  url(r'^ledger/', include('apps.ledger.urls')),
                  url(r'^voucher/', include('apps.voucher.urls')),
                  url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
                  url(r'^bank/', include('apps.bank.urls', namespace='bank')),
                  url(r'^report/', include('apps.report.urls', namespace='report')),
                  url(r'^njango/', include('njango.urls')),

                  url(r'^api-token-auth/', views.obtain_auth_token)
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler400 = 'apps.users.views.bad_request'
handler403 = 'apps.users.views.permission_denied'
handler404 = 'apps.users.views.page_not_found'
handler500 = 'apps.users.views.server_error'
