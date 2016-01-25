from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import api
import views

web_urls = [
    # url(r'^settings/$', views.bank_settings, name='bank_settings'),

    # url(r'^book/(?P<id>[0-9]+)$', views.bank_book, name='bank_book'),

    url(r'^cash_deposits/$', views.CashDepositeList.as_view(), name='cash_deposit_list'),
    url(r'^cash_deposit/add$', views.cash_deposit, name='cash_deposit_add'),
    url(r'^cash_deposit/(?P<id>[0-9]+)$', views.cash_deposit, name='cash_deposit_edit'),
    url(r'^cash_deposit/delete/(?P<pk>[0-9]+)$', views.CashDepositDelete.as_view(),
        name='cash_deposit_delete'),

    # url(r'^cheque-payments/$', views.list_cheque_payments, name='list_cheque_payments'),
    # url(r'^cheque-payment/$', views.cheque_payment, name='new_cheque_payment'),
    # url(r'^cheque-payment/(?P<id>[0-9]+)$', views.cheque_payment, name='update_cheque_payment'),
    # url(r'^cheque-payment/delete/(?P<id>[0-9]+)$', views.delete_cheque_payment,
    #     name='delete_cheque_payment'),

    url(r'^account/$', views.BankAccountList.as_view(), name='bankaccount_list'),
    url(r'^account/add/$', views.BankAccountCreate.as_view(), name='bankaccount_add'),
    url(r'^account/edit/(?P<pk>\d+)/$', views.BankAccountUpdate.as_view(), name='bankaccount_edit'),
    url(r'^account/delete/(?P<pk>\d+)/$', views.BankAccountDelete.as_view(), name='bankaccount_delete'),

    url(r'^cheque_deposit/$', views.ChequeDepositList.as_view(), name='cheque_deposit_list'),
    url(r'^cheque_deposit/add/$', views.cheque_deposit_create, name='cheque_deposit_add'),
    url(r'^cheque_deposit/(?P<id>[0-9]+)/$', views.cheque_deposit_create, name='cheque_deposit_edit'),
    url(r'^save/cheque_deposit/$', views.cheque_deposit_save, name='cheque_deposit_save'),
    url(r'^cheque_deposit/delete/(?P<pk>[0-9]+)$', views.ChequeDepositDelete.as_view(), name='cheque_deposit_delete'),
    url(r'^cheque_deposit/detail/(?P<pk>[0-9]+)/$', views.ChequeDepositDetailView.as_view(), name='cheque_deposit_detail'),

]

api_urls = [
    url(r'^api/cheque_deposits/$', api.ChequeDepositListAPI.as_view()),
    url(r'^api/cheque_deposit/(?P<pk>[0-9]+)/$', api.ChequeDepositDetailAPI.as_view()),
]

api_urls = format_suffix_patterns(api_urls)

urlpatterns = web_urls + api_urls
