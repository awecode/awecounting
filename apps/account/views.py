from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from awecounting.utils.mixins import DeleteView, UpdateView, CreateView, AjaxableResponseMixin
from .models import JournalVoucher, JournalVoucherRow
from .forms import JournalVoucherForm
from .serializer import JournalVoucherSerializer, JournalVoucherRowSerializer
from django.http import JsonResponse
from awecounting.utils.helpers import save_model, invalid, empty_to_none, delete_rows
import json


class JournalVoucherView(object):
	model = JournalVoucher
	success_url = reverse_lazy('account:journal_voucher_list')
	form_class = JournalVoucherForm

class JournalVoucherList(JournalVoucherView, ListView):
	pass


class JournalVoucherCreate(JournalVoucherView, CreateView):
	pass


def journal_voucher_create(request, id=None):
    if id:
        journal_voucher = get_object_or_404(JournalVoucher, id=id)
        scenario = 'Update'
    else:
        journal_voucher = JournalVoucher(company=request.company)
        scenario = 'Create'
    data = JournalVoucherSerializer(journal_voucher).data
    return render(request, 'account/journal_voucher_form.html', {'data': data, 'scenario': scenario})

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
