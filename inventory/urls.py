from django.conf.urls import patterns, url
import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
                       url(r'^purchase/create/$', views.create_purchase, name='purchase-create'),

                       # djangorestframework api
                       url(r'^api/item/$', views.ItemList.as_view()),
                       url(r'^api/parties/$', views.PartyList.as_view()),

)

urlpatterns = format_suffix_patterns(urlpatterns)