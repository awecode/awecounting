from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from apps.ledger.models import Account, JournalEntry
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from awecounting.utils.mixins import DeleteView, UpdateView, CreateView, AjaxableResponseMixin
from .models import JournalVoucher, JournalVoucherRow
from .forms import JournalVoucherForm
from .serializer import AccountSerializer, JournalVoucherSerializer, JournalVoucherRowSerializer
from django.http import JsonResponse
from awecounting.utils.helpers import save_model, invalid, empty_to_none, delete_rows
import json



def list_accounts(request):
    objects = Account.objects.filter()
    return render(request, 'list_accounts.html', {'accounts': objects})


def view_account(request, id):
    account = get_object_or_404(Account, id=id)
    # transactions = account.transactions
    base_template = 'dashboard.html'
    journal_entries = JournalEntry.objects.filter(transactions__account_id=account.id).order_by('id',
                                                                                                'date') \
        .prefetch_related('transactions', 'content_type', 'transactions__account').select_related()
    return render(request, 'view_account.html', {
        'account': account,
        # 'transactions': transactions.all(),
        'journal_entries': journal_entries,
        'base_template': base_template,
    })


class JournalVoucherView(object):
    model = JournalVoucher
    success_url = reverse_lazy('journal_voucher_list')
    form_class = JournalVoucherForm


class JournalVoucherList(JournalVoucherView, ListView):
    pass


def journal_voucher_create(request, id=None):
    if id:
        journal_voucher = get_object_or_404(JournalVoucher, id=id)
        scenario = 'Update'
    else:
        journal_voucher = JournalVoucher(company=request.company)
        scenario = 'Create'
    data = JournalVoucherSerializer(journal_voucher).data
    return render(request, 'ledger/journal_voucher_form.html', {'data': data, 'scenario': scenario})

def journal_voucher_save(request):
    if request.is_ajax():
        params = json.loads(request.body)
    dct = {'rows': {}}
    company = request.company
    if params.get('voucher_no') == '':
        params['voucher_no'] = None
    object_values = {'voucher_no': int(params.get('voucher_no')), 'date': params.get('date'), 'narration': params.get('narration'),
                     'status': params.get('status'), 'company': company}

    if params.get('id'):
        obj = JournalVoucher.objects.get(id=params.get('id'), company=request.company)
    else:
        obj = JournalVoucher(company=request.company)
    try:
        obj = save_model(obj, object_values)
        dct['id'] = obj.id

        model = JournalVoucherRow
        for ind, row in enumerate(params.get('table_view').get('rows')):
            if invalid(row, ['account']):
                continue
            else:
                values = {'type': row.get('type'), 'account_id': row.get('account'),
                          'description': row.get('description'), 'dr_amount': empty_to_none(float(row.get('dr_amount'))), 'cr_amount': empty_to_none(float(row.get('cr_amount'))),
                          'journal_voucher': obj}
                submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
                if not created:
                    submodel = save_model(submodel, values)
                dct['rows'][ind] = submodel.id
    except Exception as e:
        if hasattr(e, 'messages'):
            dct['error_message'] = '; '.join(e.messages)
        elif str(e) != '':
            dct['error_message'] = str(e)
        else:
            dct['error_message'] = 'Error in form data!'
    delete_rows(params.get('table_view').get('deleted_rows'), model)
    return JsonResponse(dct)

# rest_framework API
class AccountListAPI(generics.ListCreateAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()