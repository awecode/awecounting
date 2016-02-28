from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import api
import views

web_urls = [
    url(r'^cash_deposits/$', views.CashDepositList.as_view(), name='cash_deposit_list'),
    url(r'^cash_deposit/add$', views.CashDepositCreate.as_view(), name='cash_deposit_add'),
    url(r'^cash_deposit/(?P<pk>[0-9]+)$', views.CashDepositUpdate.as_view(), name='cash_deposit_edit'),
    url(r'^cash_deposit/delete/(?P<pk>[0-9]+)$', views.CashDepositDelete.as_view(),
        name='cash_deposit_delete'),

    url(r'^account/$', views.BankAccountList.as_view(), name='bankaccount_list'),
    url(r'^account/add/$', views.BankAccountCreate.as_view(), name='bankaccount_add'),
    url(r'^account/edit/(?P<pk>\d+)/$', views.BankAccountUpdate.as_view(), name='bankaccount_edit'),
    url(r'^account/delete/(?P<pk>\d+)/$', views.BankAccountDelete.as_view(), name='bankaccount_delete'),

    url(r'^cheque_deposit/$', views.ChequeDepositList.as_view(), name='cheque_deposit_list'),
    url(r'^cheque_deposit/add/$', views.ChequeDepositCreate.as_view(), name='cheque_deposit_add'),
    url(r'^cheque_deposit/(?P<pk>[0-9]+)/$', views.ChequeDepositCreate.as_view(), name='cheque_deposit_edit'),
    url(r'^save/cheque_deposit/$', views.cheque_deposit_save, name='cheque_deposit_save'),
    url(r'^cheque_deposit/delete/(?P<pk>[0-9]+)$', views.ChequeDepositDelete.as_view(), name='cheque_deposit_delete'),
    url(r'^cheque_deposit/detail/(?P<pk>[0-9]+)/$', views.ChequeDepositDetailView.as_view(), name='cheque_deposit_detail'),

    url(r'^cheque_payment/$', views.ChequePaymentList.as_view(), name='cheque_payment_list'),
    url(r'^cheque_payment/add/$', views.ChequePaymentCreate.as_view(), name='cheque_payment_add'),
    url(r'^cheque_payment/edit/(?P<pk>\d+)/$', views.ChequePaymentUpdate.as_view(), name='cheque_payment_edit'),
    url(r'^cheque_payment/delete/(?P<pk>\d+)/$', views.ChequePaymentDelete.as_view(), name='cheque_payment_delete'),

]

api_urls = [
    url(r'^api/cheque_deposits/$', api.ChequeDepositListAPI.as_view()),
    url(r'^api/cheque_deposit/(?P<pk>[0-9]+)/$', api.ChequeDepositDetailAPI.as_view()),
    url(r'^api/bank_accounts/$', api.BankAccountListAPI.as_view()),
    url(r'^api/bank_account/(?P<pk>[0-9]+)/$', api.BankAccountDetailAPI.as_view()),
    url(r'^api/bank_cash_deposits/$', api.BankCashDepositListAPI.as_view()),
    url(r'^api/bank_cash_deposit/(?P<pk>[0-9]+)/$', api.BankCashDepositDetailAPI.as_view()),
    url(r'^api/cheque_payments/$', api.ChequePaymentListAPI.as_view()),
    url(r'^api/cheque_payment/(?P<pk>[0-9]+)/$', api.ChequePaymentDetailAPI.as_view()),
]

api_urls = format_suffix_patterns(api_urls)

urlpatterns = web_urls + api_urls
