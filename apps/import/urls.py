from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

web_urls = [
]

api_urls = [
]

api_urls = format_suffix_patterns(api_urls)

urlpatterns = web_urls + api_urls
