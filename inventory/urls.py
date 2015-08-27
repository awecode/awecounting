from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^purchase/create/$', views.create_purchase, name='purchase-create'),
)