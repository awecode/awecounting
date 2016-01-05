import datetime
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
import json
from ..inventory.models import set_transactions
from ..ledger.models import set_transactions as set_ledger_transactions, Account
from awecounting.utils.helpers import save_model, invalid, empty_to_none, delete_rows, zero_for_none, write_error

from .forms import CashReceiptForm, JournalVoucherForm
from .serializers import CashReceiptSerializer, JournalVoucherSerializer, PurchaseSerializer, SaleSerializer
from .models import CashReceipt, Purchase, JournalVoucher, JournalVoucherRow, PurchaseRow, Sale, SaleRow, CashReceiptRow


@login_required
def cash_receipt(request, pk=None):
    if pk:
        voucher = get_object_or_404(CashReceipt, pk=pk, company=request.company)
        scenario = 'Update'
    else:
        voucher = CashReceipt(company=request.company)
        scenario = 'Create'
    form = CashReceiptForm(instance=voucher, company=request.company)
    data = CashReceiptSerializer(voucher).data
    return render(request, 'cash_receipt.html', {'form': form, 'scenario': scenario, 'data': data})


def purchase_list(request):
    obj = Purchase.objects.all()
    return render(request, 'purchase_list.html', {'objects': obj})


def purchase(request, id=None):
    if id:
        obj = get_object_or_404(Purchase, id=id)
        scenario = 'Update'
    else:
        obj = Purchase(company=request.company)
        scenario = 'Create'
    data = PurchaseSerializer(obj).data
    return render(request, 'purchase-form.html', {'data': data, 'scenario': scenario, 'purchase': obj})


@login_required
def save_cash_receipt(request):
    params = json.loads(request.body)
    dct = {'rows': {}}
    if params.get('voucher_no') == '':
        params['voucher_no'] = None
    object_values = {'party_id': params.get('party_id'), 'receipt_on': params.get('receipt_on'),
                     'voucher_no': params.get('voucher_no'),
                     'reference': params.get('reference'), 'company': request.company}
    if params.get('id'):
        obj = CashReceipt.objects.get(id=params.get('id'), company=request.company)
    else:
        obj = CashReceipt(company=request.company)
    try:
        obj = save_model(obj, object_values)
        dct['id'] = obj.id
        model = CashReceiptRow
        cash_account = Account.objects.get(name='Cash', company=request.company)
        if params.get('table_vm').get('rows'):
            total = 0
            for index, row in enumerate(params.get('table_vm').get('rows')):
                if invalid(row, ['payment']):
                    continue
                row['payment'] = zero_for_none(empty_to_none(row['payment']))
                invoice = Sale.objects.get(voucher_no=row.get('voucher_no'), company=request.company)
                values = {'receipt': row.get('payment'), 'cash_receipt': obj, 'invoice': invoice}
                try:
                    old_value = model.objects.get(invoice_id=row.get('id'), cash_receipt_id=obj.id).receipt or 0
                except CashReceiptRow.DoesNotExist:
                    old_value = 0
                submodel, created = model.objects.get_or_create(invoice=invoice, cash_receipt=obj, defaults=values)
                if created:
                    invoice.pending_amount -= float(row.get('payment'))
                else:
                    submodel = save_model(submodel, values)
                    invoice.pending_amount -= float(row.get('payment')) - old_value
                    invoice.save()
                dct['rows'][index] = submodel.id
                total += float(row.get('payment'))
            obj.amount = total
        else:
            obj.amount = params.get('amount')
        set_ledger_transactions(obj, obj.date,
                                ['dr', cash_account, obj.amount],
                                ['cr', obj.party.account, obj.amount]
                                )
        # obj.status = 'Unapproved'
        obj.save()
    except Exception as e:
        dct = write_error(dct, e)
    return JsonResponse(dct)


def save_purchase(request):
    if request.is_ajax():
        params = json.loads(request.body)
    dct = {'rows': {}}
    if params.get('voucher_no') == '':
        params['voucher_no'] = None
    object_values = {'voucher_no': params.get('voucher_no'), 'date': params.get('date'),
                     'party_id': params.get('party'), 'due_date': params.get('due_date'),
                     'credit': params.get('credit'), 'company': request.company}

    if params.get('id'):
        obj = Purchase.objects.get(id=params.get('id'), company=request.company)
    else:
        obj = Purchase(company=request.company)
    # if True:
    try:
        obj = save_model(obj, object_values)
        dct['id'] = obj.id

        model = PurchaseRow
        for ind, row in enumerate(params.get('table_view').get('rows')):
            if invalid(row, ['item_id', 'quantity', 'unit_id']):
                continue
            else:
                values = {'sn': ind + 1, 'item_id': row.get('item')['id'], 'quantity': row.get('quantity'),
                          'rate': row.get('rate'), 'unit_id': row.get('unit_id'), 'discount': row.get('discount'),
                          'purchase': obj}
                submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
                if not created:
                    submodel = save_model(submodel, values)
                dct['rows'][ind] = submodel.id
                set_transactions(submodel, obj.date,
                                 ['dr', submodel.item.account, submodel.quantity],
                                 )
                if obj.credit:
                    set_ledger_transactions(submodel, obj.date,
                                            ['cr', obj.party.account, obj.total],
                                            ['dr', submodel.item.ledger, obj.total],
                                            # ['cr', sales_tax_account, tax_amount],
                                            )
                else:
                    set_ledger_transactions(submodel, obj.date,
                                            ['dr', submodel.item.ledger, obj.total],
                                            ['cr', Account.objects.get(name='Cash', company=request.company),
                                             obj.total],
                                            # ['cr', sales_tax_account, tax_amount],
                                            )
                    delete_rows(params.get('table_view').get('deleted_rows'), model)

    except Exception as e:
        dct = write_error(dct, e)
    return JsonResponse(dct)


def sale(request, id=None):
    if id:
        obj = get_object_or_404(Sale, id=id)
        scenario = 'Update'
    else:
        obj = Sale(date=datetime.datetime.now().date(), company=request.company)
        scenario = 'Create'
    data = SaleSerializer(obj).data
    return render(request, 'sale_form.html', {'data': data, 'scenario': scenario, 'sale': obj})


def save_sale(request):
    if request.is_ajax():
        params = json.loads(request.body)
    dct = {'rows': {}}
    if params.get('voucher_no') == '':
        params['voucher_no'] = None
    object_values = {'voucher_no': params.get('voucher_no'), 'date': params.get('date'),
                     'party_id': params.get('party'), 'due_date': params.get('due_date'),
                     'credit': params.get('credit'), 'company': request.company}
    if params.get('id'):
        obj = Sale.objects.get(id=params.get('id'), company=request.company)
    else:
        obj = Sale(company=request.company)
    try:
        obj = save_model(obj, object_values)
        dct['id'] = obj.id
        model = SaleRow
        grand_total = 0
        for ind, row in enumerate(params.get('table_view').get('rows')):
            invalid_check = invalid(row, ['item_id', 'quantity', 'unit_id'])
            if invalid_check:
                continue
                # dct['error_message'] = 'These fields must be filled: ' + ', '.join(invalid_check)
            # else:
            values = {'sn': ind + 1, 'item_id': row.get('item')['id'], 'quantity': row.get('quantity'),
                      'rate': row.get('rate'), 'unit_id': row.get('unit_id'), 'discount': row.get('discount'),
                      'sale': obj}
            submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
            if not created:
                submodel = save_model(submodel, values)
            grand_total += submodel.get_total()
            dct['rows'][ind] = submodel.id
            set_transactions(submodel, obj.date,
                             ['cr', submodel.item.account, submodel.quantity],
                             )
            if obj.credit:
                set_ledger_transactions(submodel, obj.date,
                                        ['dr', obj.party.account, obj.total],
                                        ['cr', submodel.item.ledger, obj.total],
                                        # ['cr', sales_tax_account, tax_amount],
                                        )
            else:
                set_ledger_transactions(submodel, obj.date,
                                        ['dr', Account.objects.get(name='Cash', company=request.company), obj.total],
                                        ['cr', submodel.item.ledger, obj.total],
                                        # ['cr', sales_tax_account, tax_amount],
                                        )
                # delete_rows(params.get('table_view').get('deleted_rows'), model)
        obj.total_amount = grand_total
        if obj.credit:
            obj.pending_amount = grand_total
        obj.save()
    except Exception as e:
        dct = write_error(dct, e)
    return JsonResponse(dct)


def sale_list(request):
    objects = Sale.objects.all().prefetch_related('rows')
    return render(request, 'sale_list.html', {'objects': objects})


def sale_day(request, voucher_date):
    objects = Sale.objects.filter(date=voucher_date).prefetch_related('rows')
    total_amount = 0
    total_quantity = 0
    total_items = 0
    for obj in objects:
        for row in obj.rows.all():
            total_items += 1
            total_quantity += row.quantity
            total_amount += row.quantity * row.rate
    context = {
        'objects': objects,
        'total_amount': total_amount,
        'total_quantity': total_quantity,
        'total_items': total_items,
        'from_date': voucher_date
    }
    return render(request, 'sale_report.html', context)


def sale_date_range(request, from_date, to_date):
    objects = Sale.objects.filter(date__gte=from_date, date__lte=to_date).prefetch_related('rows')
    total_amount = 0
    total_quantity = 0
    total_items = 0
    for obj in objects:
        for row in obj.rows.all():
            total_items += 1
            total_quantity += row.quantity
            total_amount += row.quantity * row.rate
    context = {
        'objects': objects,
        'total_amount': total_amount,
        'total_quantity': total_quantity,
        'total_items': total_items,
        'from_date': from_date,
        'to_date': to_date,
    }
    return render(request, 'sale_report.html', context)


def sales_report_router(request):
    if request.GET.get('date'):
        return sale_day(request, request.GET.get('date'))
    elif request.GET.get('from') and request.GET.get('to'):
        return sale_date_range(request, request.GET.get('from'), request.GET.get('to'))
    elif request.GET.get('from'):
        return sale_day(request, request.GET.get('from'))
    else:
        return redirect(reverse_lazy('home'))


def daily_sale_today(request):
    today = datetime.date.today()
    return sale_day(request, today)


def daily_sale_yesterday(request):
    yesterday = datetime.date.today() - datetime.timedelta(1)
    return sale_day(request, yesterday)


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
    return render(request, 'voucher/journal_voucher_form.html', {'data': data, 'scenario': scenario})


def journal_voucher_save(request):
    if request.is_ajax():
        params = json.loads(request.body)
    dct = {'rows': {}}
    company = request.company
    if params.get('voucher_no') == '':
        params['voucher_no'] = None
    object_values = {'voucher_no': int(params.get('voucher_no')), 'date': params.get('date'),
                     'narration': params.get('narration'),
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
                          'description': row.get('description'), 'dr_amount': empty_to_none(float(row.get('dr_amount'))),
                          'cr_amount': empty_to_none(float(row.get('cr_amount'))),
                          'journal_voucher': obj}
                submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
                if not created:
                    submodel = save_model(submodel, values)
                dct['rows'][ind] = submodel.id
    except Exception as e:
        dct = write_error(dct, e)
    delete_rows(params.get('table_view').get('deleted_rows'), model)
    return JsonResponse(dct)
