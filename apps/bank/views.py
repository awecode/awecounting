from datetime import date
import json
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from bank.models import BankAccount, ChequeDeposit, ChequeDepositRow, BankCashDeposit, ChequePayment, ElectronicFundTransferIn, ElectronicFundTransferInRow, ElectronicFundTransferOut
from bank.forms import BankAccountForm, ChequeDepositForm, BankCashDepositForm, ChequePaymentForm, ElectronicFundTransferInForm, ElectronicFundTransferOutForm
from acubor.lib import invalid, save_model
from bank.serializers import ChequeDepositSerializer, ElectronicFundTransferInSerializer
from bank.filters import ChequeDepositFilter, CashDepositFilter, ChequePaymentFilter, ElectronicFundTransferInFilter, ElectronicFundTransferOutFilter
from ledger.models import set_transactions, Account, delete_rows, JournalEntry
from ledger.serializers import AccountSerializer
from users.models import group_required


@login_required
def bank_settings(request):
    items = BankAccount.objects.filter(company=request.company)
    return render(request, 'bank_settings.html', {'items': items})


@login_required
def list_bank_accounts(request):
    items = BankAccount.objects.filter(company=request.company)
    return render(request, 'list_bank_accounts.html', {'items': items})


@login_required
def delete_bank_account(request, id):
    obj = get_object_or_404(BankAccount, id=id, company=request.company)
    obj.delete()
    return redirect('/bank/accounts/')


@login_required
def delete_cheque_deposit(request, id):
    obj = get_object_or_404(ChequeDeposit, id=id, company=request.company)
    obj.delete()
    return redirect('/bank/cheque-deposits/')


@login_required
def delete_electronic_fund_transfer_in(request, id):
    obj = get_object_or_404(ElectronicFundTransferIn, id=id, company=request.company)
    obj.delete()
    return redirect('/bank/electronic-fund-transfers-in/')


@login_required
def delete_cash_deposit(request, id):
    obj = get_object_or_404(BankCashDeposit, id=id, company=request.company)
    obj.delete()
    return redirect('/bank/cash-deposits/')


@login_required
def delete_cheque_payment(request, id):
    obj = get_object_or_404(ChequePayment, id=id, company=request.company)
    obj.delete()
    return redirect('/bank/cheque-payments/')


@login_required
def delete_electronic_fund_transfer_out(request, id):
    obj = get_object_or_404(ElectronicFundTransferOut, id=id, company=request.company)
    obj.delete()
    return redirect('/bank/electronic-fund-transfers-out/')


@login_required
def list_cheque_deposits(request):
    items = ChequeDeposit.objects.filter(company=request.company)
    filtered_items = ChequeDepositFilter(request.GET, queryset=items, company=request.company)
    return render(request, 'list_cheque_deposits.html', {'objects': filtered_items})


@login_required
def list_cheque_payments(request):
    items = ChequePayment.objects.filter(company=request.company)
    filtered_items = ChequePaymentFilter(request.GET, queryset=items, company=request.company)
    return render(request, 'list_cheque_payments.html', {'objects': filtered_items})


@login_required
def list_electronic_fund_transfers_in(request):
    items = ElectronicFundTransferIn.objects.filter(company=request.company)
    filtered_items = ElectronicFundTransferInFilter(request.GET, queryset=items, company=request.company)
    return render(request, 'list_electronic_fund_transfers_in.html', {'objects': filtered_items})


@login_required
def list_electronic_fund_transfers_out(request):
    items = ElectronicFundTransferOut.objects.filter(company=request.company)
    filtered_items = ElectronicFundTransferOutFilter(request.GET, queryset=items, company=request.company)
    return render(request, 'list_electronic_fund_transfers_out.html', {'objects': filtered_items})


@login_required
def list_cash_deposits(request):
    items = BankCashDeposit.objects.filter(company=request.company)
    filtered_items = CashDepositFilter(request.GET, queryset=items, company=request.company)
    return render(request, 'list_cash_deposits.html', {'objects': filtered_items})


@login_required
def bank_account_form(request, id=None):
    if id:
        bank_account = get_object_or_404(BankAccount, id=id, company=request.company)
        scenario = 'Update'
    else:
        bank_account = BankAccount()
        scenario = 'Create'
    if request.POST:
        form = BankAccountForm(data=request.POST, instance=bank_account)
        if form.is_valid():
            item = form.save(commit=False)
            item.company = request.company
            item.save()
            if request.is_ajax():
                return render(request, 'callback.html', {'obj': AccountSerializer(item.account).data})
            return redirect('/bank/accounts/')
    else:
        form = BankAccountForm(instance=bank_account)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'
    return render(request, 'bank_account_form.html', {
        'scenario': scenario,
        'form': form,
        'base_template': base_template,
    })


@login_required
def cash_deposit(request, id=None):
    if id:
        receipt = get_object_or_404(BankCashDeposit, id=id, company=request.company)
        scenario = 'Update'
    else:
        receipt = BankCashDeposit(date=date.today(), company=request.company)
        scenario = 'New'
    if request.POST.get('action') == 'Approve':
        set_transactions(receipt, receipt.date,
                         ['dr', receipt.bank_account, receipt.amount],
                         ['cr', receipt.benefactor, receipt.amount],
        )
        receipt.status = 'Approved'
        receipt.save()
        return redirect(reverse_lazy('update_cash_deposit', kwargs={'id': receipt.id}))
    if request.POST:
        form = BankCashDepositForm(request.POST, initial={'voucher_no': 20}, instance=receipt, company=request.company)
        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.company = request.company
            if 'attachment' in request.FILES:
                receipt.attachment = request.FILES['attachment']
            receipt.status = 'Unapproved'
            receipt.save()
            return redirect(reverse_lazy('update_cash_deposit', kwargs={'id': receipt.id}))
    else:
        form = BankCashDepositForm(instance=receipt, company=request.company)
    return render(request, 'cash_deposit.html', {'form': form, 'scenario': scenario})


@login_required
def cheque_deposit(request, id=None):
    if id:
        receipt = get_object_or_404(ChequeDeposit, id=id, company=request.company)
        scenario = 'Update'
    else:
        receipt = ChequeDeposit(date=date.today(), company=request.company)
        scenario = 'New'
    if request.POST:
        form = ChequeDepositForm(request.POST, request.FILES, instance=receipt, company=request.company)
        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.company = request.company
            if 'attachment' in request.FILES:
                receipt.attachment = request.FILES['attachment']
            receipt.status = 'Unapproved'
            receipt.save()
            particulars = json.loads(request.POST['particulars'])
            model = ChequeDepositRow
            for index, row in enumerate(particulars.get('rows')):
                if invalid(row, ['amount']):
                    continue
                values = {'sn': index + 1, 'cheque_number': row.get('cheque_number'),
                          'cheque_date': row.get('cheque_date'),
                          'drawee_bank': row.get('drawee_bank'), 'drawee_bank_address': row.get('drawee_bank_address'),
                          'amount': row.get('amount'), 'cheque_deposit': receipt}
                submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
                if not created:
                    submodel = save_model(submodel, values)
            delete_rows(particulars.get('deleted_rows'), model)
            return redirect(reverse_lazy('update_cheque_deposit', kwargs={'id': receipt.id}))
            #else: #do not suggest voucher number
            #    receipt.voucher_no = form['voucher_no'].value()
    else:
        form = ChequeDepositForm(instance=receipt, company=request.company)
    receipt_data = ChequeDepositSerializer(receipt).data
    return render(request, 'cheque_deposit.html', {'form': form, 'data': receipt_data, 'scenario': scenario})


@login_required
def electronic_fund_transfer_in(request, id=None):
    if id:
        receipt = get_object_or_404(ElectronicFundTransferIn, id=id, company=request.company)
        scenario = 'Update'
    else:
        receipt = ElectronicFundTransferIn(date=date.today(), company=request.company)
        scenario = 'New'
    if request.POST:
        form = ElectronicFundTransferInForm(request.POST, request.FILES, instance=receipt, company=request.company)
        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.company = request.company
            if 'attachment' in request.FILES:
                receipt.attachment = request.FILES['attachment']
            receipt.status = 'Unapproved'
            receipt.save()
        if id or form.is_valid():
            particulars = json.loads(request.POST['particulars'])
            model = ElectronicFundTransferInRow
            bank_account = Account.objects.get(id=request.POST.get('bank_account'))
            benefactor = Account.objects.get(id=request.POST.get('benefactor'))
            for index, row in enumerate(particulars.get('rows')):
                if invalid(row, ['amount']):
                    continue
                values = {'sn': index + 1, 'transaction_number': row.get('transaction_number'),
                          'transaction_date': row.get('transaction_date'),
                          'drawee_bank': row.get('drawee_bank'), 'drawee_bank_address': row.get('drawee_bank_address'),
                          'amount': row.get('amount'), 'electronic_fund_transfer_in': receipt}
                submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
                #set_transactions(submodel, request.POST.get('date'),
                #                 ['dr', bank_account, row.get('amount')],
                #                 ['cr', benefactor, row.get('amount')],
                #)
                if not created:
                    submodel = save_model(submodel, values)
            delete_rows(particulars.get('deleted_rows'), model)
            return redirect(reverse_lazy('update_electronic_fund_transfer_in', kwargs={'id': receipt.id}))
    else:
        form = ElectronicFundTransferInForm(instance=receipt, company=request.company)
    receipt_data = ElectronicFundTransferInSerializer(receipt).data
    return render(request, 'electronic_fund_transfer_in.html',
                  {'form': form, 'data': receipt_data, 'scenario': scenario})


@group_required('SuperOwner', 'Owner', 'Supervisor')
def approve_eft_in(request):
    params = json.loads(request.body)
    dct = {}
    if params.get('id'):
        voucher = ElectronicFundTransferIn.objects.get(id=params.get('id'))
    else:
        dct['error_message'] = 'Voucher needs to be saved before being approved!'
        return HttpResponse(json.dumps(dct), mimetype="application/json")
    bank_account = Account.objects.get(id=params.get('bank_account'))
    benefactor = Account.objects.get(id=params.get('benefactor'))
    for row in voucher.rows.all():
        set_transactions(row, params.get('date'),
                         ['dr', bank_account, row.amount],
                         ['cr', benefactor, row.amount],
        )
    voucher.status = 'Approved'
    voucher.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@group_required('SuperOwner', 'Owner', 'Supervisor')
def approve_cheque_deposit(request):
    params = json.loads(request.body)
    dct = {}
    if params.get('id'):
        voucher = ChequeDeposit.objects.get(id=params.get('id'))
    else:
        dct['error_message'] = 'Voucher needs to be saved before being approved!'
        return HttpResponse(json.dumps(dct), mimetype="application/json")
    bank_account = Account.objects.get(id=params.get('bank_account'))
    benefactor = Account.objects.get(id=params.get('benefactor'))
    for row in voucher.rows.all():
        set_transactions(row, params.get('date'),
                         ['dr', bank_account, row.amount],
                         ['cr', benefactor, row.amount],
        )
    voucher.status = 'Approved'
    voucher.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def cheque_payment(request, id=None):
    if id:
        payment = get_object_or_404(ChequePayment, id=id, company=request.company)
        scenario = 'Update'
    else:
        payment = ChequePayment(date=date.today())
        scenario = 'New'
    if request.POST.get('action') == 'Approve':
        set_transactions(payment, payment.date,
                         ['cr', payment.bank_account, payment.amount],
                         ['dr', payment.beneficiary, payment.amount],
        )
        payment.status = 'Approved'
        payment.save()
        return redirect(reverse_lazy('update_cheque_payment', kwargs={'id': payment.id}))
    if request.POST:
        form = ChequePaymentForm(request.POST, request.FILES, instance=payment, company=request.company)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.company = request.company
            if 'attachment' in request.FILES:
                payment.attachment = request.FILES['attachment']
            payment.status = 'Unapproved'
            payment.save()
            return redirect(reverse_lazy('update_cheque_payment', kwargs={'id': payment.id}))
    else:
        form = ChequePaymentForm(instance=payment, company=request.company)
    return render(request, 'cheque_payment.html', {'form': form, 'scenario': scenario})


@login_required
def electronic_fund_transfer_out(request, id=None):
    if id:
        payment = get_object_or_404(ElectronicFundTransferOut, id=id, company=request.company)
        scenario = 'Update'
    else:
        payment = ElectronicFundTransferOut(date=date.today())
        scenario = 'New'
    if request.POST.get('action') == 'Approve':
        set_transactions(payment, payment.date,
                         ['cr', payment.bank_account, payment.amount],
                         ['dr', payment.beneficiary, payment.amount],
        )
        payment.status = 'Approved'
        payment.save()
        return redirect(reverse_lazy('update_electronic_fund_transfer_out', kwargs={'id': payment.id}))
    if request.POST:
        form = ElectronicFundTransferOutForm(request.POST, request.FILES, instance=payment, company=request.company)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.company = request.company
            print request.POST
            if 'attachment' in request.FILES:
                payment.attachment = request.FILES['attachment']
            payment.status = 'Unapproved'
            payment.save()
            return redirect(reverse_lazy('update_electronic_fund_transfer_out', kwargs={'id': payment.id}))
    else:
        form = ElectronicFundTransferOutForm(instance=payment, company=request.company)
    return render(request, 'electronic_fund_transfer_out.html', {'form': form, 'scenario': scenario})


@login_required
def bank_book(request, id):
    bank_account = BankAccount.objects.get(id=id)
    account = bank_account.account
    journal_entries = JournalEntry.objects.filter(transactions__account_id=account.id).order_by('id',
                                                                                                'date') \
        .prefetch_related('transactions', 'content_type', 'transactions__account').select_related()
    return render(request, 'bank_book.html',
                  {'account': account, 'bank_account': bank_account, 'journal_entries': journal_entries})
