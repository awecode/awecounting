from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from ..voucher.forms import CashReceiptForm
from ..voucher.serializers import CashReceiptSerializer
from .models import CashReceipt
from datetime import date


@login_required
def cash_receipt(request, id=None):
    if id:
        voucher = get_object_or_404(CashReceipt, id=id, company=request.company)
        scenario = 'Update'
    else:
        voucher = CashReceipt(company=request.company, date=date.today())
        scenario = 'Create'
    form = CashReceiptForm(instance=voucher, company=request.company)
    data = CashReceiptSerializer(voucher).data
    return render(request, 'cash_receipt.html', {'form': form, 'scenario': scenario, 'data': data})


# @login_required
# def party_invoices(request, id):
#     objs = Invoice.objects.filter(company=request.company, party=Party.objects.get(id=id), pending_amount__gt=0)
#     lst = []
#     for obj in objs:
#         lst.append({'id': obj.id, 'bill_no': obj.invoice_no, 'date': obj.date, 'total_amount': obj.total_amount,
#                     'pending_amount': obj.pending_amount, 'due_date': obj.due_date})
#     return HttpResponse(json.dumps(lst, default=handler), mimetype="application/json")
#
#
# @login_required
# def save_cash_receipt(request):
#     params = json.loads(request.body)
#     dct = {'rows': {}}
#
#     # try:
#     if params.get('id'):
#         voucher = CashReceipt.objects.get(id=params.get('id'), company=request.company)
#     else:
#         voucher = CashReceipt(company=request.company)
#         # if not created:
#     try:
#         existing = CashReceipt.objects.get(voucher_no=params.get('voucher_no'), company=request.company)
#         if voucher.id is not existing.id:
#             return HttpResponse(json.dumps({'error_message': 'Voucher no. already exists'}),
#                                 mimetype="application/json")
#     except CashReceipt.DoesNotExist:
#         pass
#     values = {'party_id': params.get('party'), 'receipt_on': params.get('receipt_on'),
#               'voucher_no': params.get('voucher_no'),
#               'reference': params.get('reference'), 'company': request.company}
#     voucher = save_model(voucher, values)
#     dct['id'] = voucher.id
#     # except Exception as e:
#     #
#     #     if hasattr(e, 'messages'):
#     #         dct['error_message'] = '; '.join(e.messages)
#     #     else:
#     #         dct['error_message'] = 'Error in form data!'
#     model = CashReceiptRow
#     if params.get('table_vm').get('rows'):
#         for index, row in enumerate(params.get('table_vm').get('rows')):
#             if invalid(row, ['payment']) and invalid(row, ['discount']):
#                 continue
#             if (row.get('discount') == '') | (row.get('discount') is None):
#                 row['discount'] = 0
#             if (row.get('payment') == '') | (row.get('payment') is None):
#                 row['payment'] = 0
#             invoice = Invoice.objects.get(invoice_no=row.get('bill_no'), company=request.company)
#             values = {'discount': row.get('discount'), 'receipt': row.get('payment'),
#                       'cash_receipt': voucher,
#                       'invoice': invoice}
#             submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
#             if not created:
#                 submodel = save_model(submodel, values)
#             dct['rows'][index] = submodel.id
#         total = float(params.get('total_payment')) + float(params.get('total_discount'))
#         voucher.amount = total
#         voucher.status = 'Unapproved'
#         voucher.save()
#     else:
#         voucher.amount = params.get('amount')
#         voucher.status = 'Unapproved'
#         voucher.save()
#     if params.get('continue'):
#         dct = {'redirect_to': str(reverse_lazy('create_cash_receipt'))}
#     return HttpResponse(json.dumps(dct), mimetype="application/json")
