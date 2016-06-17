from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

web_urls = [
    url(r'^import_debtor_tally/$', views.import_debtor_tally, name='import_debtor_tally'),
    url(r'^import_stock_tally/$', views.import_stock_tally, name='import_stock_tally')
]

api_urls = [
]

api_urls = format_suffix_patterns(api_urls)

urlpatterns = web_urls + api_urls
