from django.conf.urls import url
import views

urlpatterns = [
                       # url(r'^settings/$', views.bank_settings, name='bank_settings'),
                       # url(r'^accounts/$', views.list_bank_accounts, name='list_bank_accounts'),
                       # url(r'^account/create/$', views.bank_account_form, name='create_bank_account'),
                       # url(r'^account/update/(?P<id>[0-9]+)$', views.bank_account_form, name='update_bank_account'),
                       # url(r'^account/delete/(?P<id>[0-9]+)$', views.delete_bank_account, name='delete_bank_account'),

                       # url(r'^book/(?P<id>[0-9]+)$', views.bank_book, name='bank_book'),

                       # url(r'^cheque-deposits/$', views.list_cheque_deposits, name='list_cheque_deposits'),
                       # url(r'^cheque-deposit/$', views.cheque_deposit, name='new_cheque_deposit'),
                       # url(r'^cheque-deposit/(?P<id>[0-9]+)$', views.cheque_deposit, name='update_cheque_deposit'),
                       # url(r'^cheque-deposit/delete/(?P<id>[0-9]+)$', views.delete_cheque_deposit,
                       #     name='delete_cheque_deposit'),
                       # url(r'^cheque-deposit/approve/$', views.approve_cheque_deposit, name='approve_cheque_deposit'),


                       url(r'^cash-deposits/$', views.list_cash_deposits, name='list_cash_deposits'),
                       url(r'^cash-deposit/$', views.cash_deposit, name='new_cash_deposit'),
                       url(r'^cash-deposit/(?P<id>[0-9]+)$', views.cash_deposit, name='update_cash_deposit'),
                       url(r'^cash-deposit/delete/(?P<id>[0-9]+)$', views.delete_cash_deposit,
                           name='delete_cash_deposit'),

                       # url(r'^cheque-payments/$', views.list_cheque_payments, name='list_cheque_payments'),
                       # url(r'^cheque-payment/$', views.cheque_payment, name='new_cheque_payment'),
                       # url(r'^cheque-payment/(?P<id>[0-9]+)$', views.cheque_payment, name='update_cheque_payment'),
                       # url(r'^cheque-payment/delete/(?P<id>[0-9]+)$', views.delete_cheque_payment,
                       #     name='delete_cheque_payment'),

                       # url(r'^electronic-fund-transfers-out/$', views.list_electronic_fund_transfers_out,
                       #     name='list_electronic_fund_transfers_out'),
                       # url(r'^electronic-fund-transfer-out/$', views.electronic_fund_transfer_out,
                       #     name='new_electronic_fund_transfer_out'),
                       # url(r'^electronic-fund-transfer-out/(?P<id>[0-9]+)$', views.electronic_fund_transfer_out,
                       #     name='update_electronic_fund_transfer_out'),
                       # url(r'^electronic-fund-transfer-out/delete/(?P<id>[0-9]+)$',
                       #     views.delete_electronic_fund_transfer_out,
                       #     name='delete_electronic_fund_transfer_out'),

                       # url(r'^electronic-fund-transfers-in/$', views.list_electronic_fund_transfers_in,
                       #     name='list_electronic_fund_transfers_in'),
                       # url(r'^electronic-fund-transfer-in/$', views.electronic_fund_transfer_in,
                       #     name='new_electronic_fund_transfer_in'),
                       # url(r'^electronic-fund-transfer-in/(?P<id>[0-9]+)$', views.electronic_fund_transfer_in,
                       #     name='update_electronic_fund_transfer_in'),
                       # url(r'^eft-in/approve/$', views.approve_eft_in, name='approve_eft_in'),
                       # url(r'^electronic-fund-transfer-in/delete/(?P<id>[0-9]+)$',
                       #     views.delete_electronic_fund_transfer_in,
                       #     name='delete_electronic_fund_transfer_in'),
                       url(r'^account/$', views.BankAccountList.as_view(), name='bankaccount_list'),
                       url(r'^account/add/$', views.BankAccountCreate.as_view(), name='bankaccount_add'),
                       url(r'^account/edit/(?P<pk>\d+)/$', views.BankAccountUpdate.as_view(), name='bankaccount_edit'),
                       url(r'^account/delete/(?P<pk>\d+)/$', views.BankAccountDelete.as_view(), name='bankaccount_delete'),

]
