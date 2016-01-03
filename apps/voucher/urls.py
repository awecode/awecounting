from django.conf.urls import url

import views

urlpatterns = [
    url(r'^cash_receipt/$', views.cash_receipt, name='create_cash_receipt'),
]
