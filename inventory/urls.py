from django.conf.urls import patterns, url
import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
                       url(r'^purchase/create/$', views.create_purchase, name='purchase-create'),
                       url(r'^save/purchase/$', views.save_purchase, name='purchase-save'),


                       url(r'^api/items/$', views.ItemList.as_view()),
                       url(r'^api/parties/$', views.PartyList.as_view()),
                       url(r'^api/units/$', views.UnitList.as_view()),


)

urlpatterns = format_suffix_patterns(urlpatterns)