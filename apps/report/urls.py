from django.conf.urls import url
import views

web_urls = [
    url(r'^trial_balance/$', views.trial_balance, name='trial_balance'),
]

urlpatterns = web_urls
