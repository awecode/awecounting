from django.conf.urls import url

import views

web_urls = [
    url(r'^report_setting/$', views.ReportSettingUpdateView.as_view(), name='report_setting'),
    url(r'^save_settings/$', views.save_report_settings, name='save_report_settings'),
    url(r'^trial_balance/$', views.trial_balance, name='trial_balance'),
    url(r'^trial_balance.json$', views.trial_balance_json, name='trial_balance_json'),
    url(r'^trading_account/$', views.trading_account, name='trading_account'),
    url(r'^profit_loss/$', views.profit_loss, name='profit_loss'),
    url(r'^balance_sheet/$', views.balance_sheet, name='balance_sheet'),
]

urlpatterns = web_urls
