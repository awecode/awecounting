import datetime
import json

from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView

from ..ledger.serializers import PartyBalanceSerializer, AccountSerializer
from ..inventory.serializers import ItemSerializer, UnitSerializer, LocationSerializer
from ..tax.serializers import TaxSchemeSerializer
from awecounting.utils.mixins import CompanyView, DeleteView, SuperOwnerMixin, group_required, TableObjectMixin, UpdateView, \
    CompanyRequiredMixin, CreateView, TableObject, CashierMixin, \
    StockistMixin, AccountantMixin
from ..inventory.models import set_transactions, Location, LocationContain, Item
from ..ledger.models import set_transactions as set_ledger_transactions, get_account, Account, Category
from awecounting.utils.helpers import save_model, invalid, empty_to_none, delete_rows, zero_for_none, write_error, mail_exception, \
    get_serialize_data
from .forms import JournalVoucherForm, VoucherSettingForm, CashPaymentForm, CashReceiptForm
from .serializers import FixedAssetSerializer, CashReceiptSerializer, \
    CashPaymentSerializer, JournalVoucherSerializer, PurchaseVoucherSerializer, SaleSerializer, PurchaseOrderSerializer, \
    ExpenseSerializer, ExportPurchaseVoucherRowSerializer
from .models import FixedAsset, FixedAssetRow, AdditionalDetail, CashReceipt, PurchaseVoucher, JournalVoucher, \
    JournalVoucherRow, \
    PurchaseVoucherRow, Sale, SaleRow, CashReceiptRow, CashPayment, CashPaymentRow, PurchaseOrder, PurchaseOrderRow, \
    VoucherSetting, Expense, ExpenseRow, TradeExpense, Lot, LotItemDetail, SaleFromLocation


class FixedAssetView(CompanyView):
    model = FixedAsset
    success_url = reverse_lazy('fixed_asset_list')
    serializer_class = FixedAssetSerializer


class FixedAssetList(FixedAssetView, AccountantMixin, ListView):
    pass


class FixedAssetDelete(FixedAssetView, AccountantMixin, DeleteView):
    pass


class FixedAssetDetailView(AccountantMixin, DetailView):
    model = FixedAsset

    def get_context_data(self, **kwargs):
        context = super(FixedAssetDetailView, self).get_context_data(**kwargs)
        context['rows'] = FixedAssetRow.objects.select_related('asset_ledger').filter(fixed_asset=self.object)
        return context


class FixedAssetCreate(FixedAssetView, AccountantMixin, TableObjectMixin):
    template_name = 'fixed_asset_form.html'

    def get_context_data(self, *args, **kwargs):
        context = super(FixedAssetCreate, self).get_context_data(**kwargs)
        context['data']['accounts'] = get_serialize_data(AccountSerializer, self.request.company)
        return context


def save_fixed_asset(request):
    if request.is_ajax():
        # params = json.loads(request.body)
        params = json.loads(request.POST.get('fixed_asset'))
    dct = {'rows': {}, 'additional_detail': {}, }
    company = request.company
    if params.get('voucher_no') == '':
        params['voucher_no'] = None
    object_values = {'voucher_no': int(params.get('voucher_no')), 'date': params.get('date'),
                     'from_account_id': params.get('from_account'),
                     'reference': params.get('reference'), 'description': params.get('description'), 'company': company}
    if params.get('id'):
        obj = FixedAsset.objects.get(id=params.get('id'), company__in=request.company.get_all())
    else:
        obj = FixedAsset(company=request.company)
    try:
        obj = save_model(obj, object_values)
        dct['id'] = obj.id
        model = FixedAssetRow
        for ind, row in enumerate(params.get('table_view').get('rows')):
            if invalid(row, ['asset_ledger', 'amount']):
                continue
            else:
                values = {'asset_ledger_id': row.get('asset_ledger'),
                          'description': row.get('description'), 'amount': row.get('amount'),
                          'fixed_asset': obj}
                submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
                if not created:
                    submodel = save_model(submodel, values)
                dct['rows'][ind] = submodel.id
        delete_rows(params.get('table_view').get('deleted_rows'), model)
        additional_detail = AdditionalDetail
        for ind, row in enumerate(params.get('additional_detail').get('rows')):
            values = {'assets_code': row.get('assets_code'), 'assets_type': row.get('assets_type'),
                      'vendor_name': row.get('vendor_name'), 'vendor_address': row.get('vendor_address'),
                      'amount': row.get('amount'), 'useful_life': row.get('useful_life'),
                      'description': row.get('description'), 'warranty_period': row.get('warranty_period'),
                      'maintenance': row.get('maintenance'), 'fixed_asset': obj}
            submodel, created = additional_detail.objects.get_or_create(id=row.get('id'), defaults=values)
            if not created:
                submodel = save_model(submodel, values)
            dct['additional_detail'][ind] = submodel.id
        delete_rows(params.get('additional_detail').get('deleted_rows'), additional_detail)
    except Exception as e:
        dct = write_error(dct, e)
        mail_exception(request)
    return JsonResponse(dct)


class CashReceiptView(CompanyView):
    model = CashReceipt
    serializer_class = CashReceiptSerializer
    form_class = CashReceiptForm


class CashReceiptList(CashReceiptView, AccountantMixin, ListView):
    pass


class CashReceiptDetailView(CashReceiptView, AccountantMixin, DetailView):
    def get_context_data(self, **kwargs):
        context = super(CashReceiptDetailView, self).get_context_data(**kwargs)
        context['rows'] = CashReceiptRow.objects.select_related('invoice').filter(cash_receipt=self.object)
        return context


class CashReceiptCreate(CashReceiptView, TableObject, AccountantMixin, CreateView):
    template_name = 'cash_receipt.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CashReceiptCreate, self).get_context_data(**kwargs)
        context['data']['parties'] = get_serialize_data(PartyBalanceSerializer, self.request.company)
        return context


class CashReceiptUpdate(CashReceiptView, TableObject, AccountantMixin, UpdateView):
    template_name = 'cash_receipt.html'


class CashPaymentView(CompanyView):
    model = CashPayment
    serializer_class = CashPaymentSerializer
    form_class = CashPaymentForm


class CashPaymentList(CashPaymentView, AccountantMixin, ListView):
    pass


class CashPaymentCreate(CashPaymentView, TableObject, AccountantMixin, CreateView):
    template_name = 'cash_payment.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CashPaymentCreate, self).get_context_data(**kwargs)
        context['data']['parties'] = get_serialize_data(PartyBalanceSerializer, self.request.company)
        return context


class CashPaymentUpdate(CashPaymentView, TableObject, AccountantMixin, UpdateView):
    template_name = 'cash_payment.html'


class CashPaymentDetailView(AccountantMixin, DetailView):
    model = CashPayment

    def get_context_data(self, **kwargs):
        context = super(CashPaymentDetailView, self).get_context_data(**kwargs)
        context['rows'] = CashPaymentRow.objects.select_related('invoice').filter(cash_payment=self.object)
        return context


# @login_required
# def cash_receipt(request, pk=None):
#     if pk:
#         voucher = get_object_or_404(CashReceipt, pk=pk, company__in=request.company.get_all())
#         scenario = 'Update'
#     else:
#         voucher = CashReceipt(company=request.company)
#         scenario = 'Create'
#     form = CashReceiptForm(instance=voucher, company=request.company)
#     data = CashReceiptSerializer(voucher).data
#     return render(request, 'cash_receipt.html', {'form': form, 'scenario': scenario, 'data': data})



# @login_required
# def cash_payment(request, pk=None):
#     if pk:
#         voucher = get_object_or_404(CashPayment, pk=pk, company__in=request.company.get_all())
#         scenario = 'Update'
#     else:
#         voucher = CashPayment(company=request.company)
#         scenario = 'Create'
#     form = CashPaymentForm(instance=voucher, company=request.company)
#     data = CashPaymentSerializer(voucher).data
#     return render(request, 'cash_payment.html', {'form': form, 'scenario': scenario, 'data': data})


def save_cash_payment(request):
    params = json.loads(request.body)
    dct = {'rows': {}}
    if params.get('voucher_no') == '':
        params['voucher_no'] = None
    object_values = {'party_id': params.get('party_id'), 'date': params.get('date'),
                     'voucher_no': params.get('voucher_no'),
                     'reference': params.get('reference'), 'company': request.company}
    if params.get('id'):
        obj = CashPayment.objects.get(id=params.get('id'), company__in=request.company.get_all())
    else:
        obj = CashPayment(company=request.company)
    try:
        obj = save_model(obj, object_values)
        dct['id'] = obj.id
        model = CashPaymentRow
        cash_account = get_account(obj.company, 'Cash')
        if params.get('table_vm').get('rows'):
            total = 0
            for index, row in enumerate(params.get('table_vm').get('rows')):
                if invalid(row, ['payment']):
                    continue
                row['payment'] = zero_for_none(empty_to_none(row['payment']))
                invoice = PurchaseVoucher.objects.get(voucher_no=row.get('voucher_no'), company__in=request.company.get_all())
                invoice.pending_amount = row.get('pending_amount')
                invoice.save()
                values = {'payment': row.get('payment'), 'cash_payment': obj, 'invoice': invoice}
                try:
                    old_value = model.objects.get(invoice_id=row.get('id'), cash_payment_id=obj.id).payment or 0
                except CashPaymentRow.DoesNotExist:
                    old_value = 0
                submodel, created = model.objects.get_or_create(invoice=invoice, cash_payment=obj, defaults=values)
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
                                ['cr', cash_account, obj.amount],
                                ['dr', obj.party.supplier_account, obj.amount]
                                )
        # obj.status = 'Unapproved'
        obj.save()
    except Exception as e:
        dct = write_error(dct, e)
        mail_exception(request)
    return JsonResponse(dct)


class PurchaseVoucherView(CompanyView):
    model = PurchaseVoucher
    serializer_class = PurchaseVoucherSerializer
    success_url = reverse_lazy("purchase-list")
    check = 'can_manage_purchases'


class SaleView(CompanyView):
    model = Sale
    serializer_class = SaleSerializer
    success_url = reverse_lazy("sale-list")
    check = 'can_manage_sales'


class PurchaseVoucherDetailView(PurchaseVoucherView, AccountantMixin, DetailView):
    def get_context_data(self, **kwargs):
        context = super(PurchaseVoucherDetailView, self).get_context_data(**kwargs)
        context['rows'] = PurchaseVoucherRow.objects.select_related('item', 'unit').filter(purchase=self.object)
        return context


class SaleDetailView(SaleView, CashierMixin, DetailView):
    def get_context_data(self, **kwargs):
        context = super(SaleDetailView, self).get_context_data(**kwargs)
        context['rows'] = SaleRow.objects.select_related('item', 'unit').filter(sale=self.object)
        return context


class JournalVoucherDetailView(CompanyView, AccountantMixin, DetailView):
    model = JournalVoucher
    check = 'can_manage_journal_vouchers'

    def get_context_data(self, **kwargs):
        context = super(JournalVoucherDetailView, self).get_context_data(**kwargs)
        context['rows'] = JournalVoucherRow.objects.filter(journal_voucher=self.object).select_related('account')
        return context


class PurchaseVoucherList(PurchaseVoucherView, AccountantMixin, ListView):
    pass


class PurchaseVoucherDelete(PurchaseVoucherView, AccountantMixin, DeleteView):
    pass


class PurchaseVoucherCreate(PurchaseVoucherView, AccountantMixin, TableObjectMixin):
    template_name = 'purchase-form.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PurchaseVoucherCreate, self).get_context_data(**kwargs)
        if not self.kwargs:
            obj = context['obj']
            tax = self.request.company.settings.purchase_default_tax_application_type
            tax_scheme = self.request.company.settings.purchase_default_tax_scheme
            if tax:
                obj.tax = tax
            if tax_scheme:
                obj.tax_scheme = tax_scheme
            data = self.serializer_class(obj).data
            item_obj = Item.objects.filter(company=self.request.company)
            item_data = ItemSerializer(item_obj, context={'request': self.request, 'voucher': 'purchase'}, many=True).data

            context['obj'] = obj
            context['data'] = data
            context['data']['tax'] = get_serialize_data(TaxSchemeSerializer, self.request.company)
            context['data']['items'] = item_data
            context['data']['units'] = get_serialize_data(UnitSerializer, self.request.company)
            context['data']['parties'] = get_serialize_data(PartyBalanceSerializer, self.request.company)
            context['data']['enable_locations'] = get_serialize_data(LocationSerializer, self.request.company,
                                                                     Location.objects.filter(
                                                                         company=self.request.company, enabled=True))
        return context


class ExportPurchaseVoucher(TemplateView):
    model = PurchaseVoucher
    serializer_class = PurchaseVoucherSerializer
    template_name = 'purchase-form.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ExportPurchaseVoucher, self).get_context_data(*args, **kwargs)
        purchase_order = PurchaseOrder.objects.get(pk=self.kwargs.get('purchase_order_pk'))
        row_data = []
        if purchase_order.purchase_voucher.all().exists():
            obj = purchase_order.purchase_voucher.all()[0]
        else:
            obj = self.model(company=self.request.company)
            obj.party = purchase_order.party
            obj.date = purchase_order.date
            tax = self.request.company.settings.purchase_default_tax_application_type
            tax_scheme = self.request.company.settings.purchase_default_tax_scheme
            if tax:
                obj.tax = tax
            if tax_scheme:
                obj.tax_scheme = tax_scheme
            rows = purchase_order.rows.filter(fulfilled=True)
            row_data = ExportPurchaseVoucherRowSerializer(rows, many=True).data
        context['data'] = self.serializer_class(obj).data
        if row_data:
            context['data']['rows'] = row_data
        context['data']['purchase_order_id'] = purchase_order.id
        context['obj'] = obj
        return context


@group_required('Accountant')
def save_cash_receipt(request):
    params = json.loads(request.body)
    dct = {'rows': {}}
    if params.get('voucher_no') == '':
        params['voucher_no'] = None
    object_values = {'party_id': params.get('party_id'), 'date': params.get('date'),
                     'voucher_no': params.get('voucher_no'),
                     'reference': params.get('reference'), 'company': request.company}
    if params.get('id'):
        obj = CashReceipt.objects.get(id=params.get('id'), company__in=request.company.get_all())
    else:
        obj = CashReceipt(company=request.company)
    try:
        obj = save_model(obj, object_values)
        dct['id'] = obj.id
        model = CashReceiptRow
        cash_account = get_account(obj.company, 'Cash')
        if params.get('table_vm').get('rows'):
            total = 0
            for index, row in enumerate(params.get('table_vm').get('rows')):
                if invalid(row, ['payment']):
                    continue
                row['payment'] = zero_for_none(empty_to_none(row['payment']))
                invoice = Sale.objects.get(voucher_no=row.get('voucher_no'), company__in=request.company.get_all())
                invoice.pending_amount = row.get('pending_amount')
                invoice.save()
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
                                ['cr', obj.party.customer_account, obj.amount]
                                )
        # obj.status = 'Unapproved'
        obj.save()
    except Exception as e:
        dct = write_error(dct, e)
        mail_exception(request)
    return JsonResponse(dct)


@group_required('Cashier')
def save_purchase(request):
    if request.is_ajax():
        params = json.loads(request.body)
    dct = {'rows': {}, 'tax': {}}

    # if not request.company.settings.discount_on_voucher:
    #     voucher_discount = None
    # else:
    #     voucher_discount = params.get('voucher_discount')
    object_values = {'voucher_no': empty_to_none(params.get('voucher_no')), 'date': params.get('date'),
                     'party_id': params.get('party_id'), 'due_date': params.get('due_date'),
                     'discount': params.get('voucher_discount'),
                     'credit': params.get('credit'), 'tax': params.get('tax'),
                     'tax_scheme_id': empty_to_none(params.get('tax_scheme_id')),
                     'purchase_order_id': empty_to_none(params.get('purchase_order_id')),
                     'company': request.company}

    if params.get('id'):
        obj = PurchaseVoucher.objects.get(id=params.get('id'), company__in=request.company.get_all())

        if request.company.settings.show_lot:
            # For Lot on edit==> delete or subtract item
            for row in obj.rows.all():
                lot = row.lot
                if lot:
                    for item in lot.lot_item_details.all():
                        if item.item == row.item:
                            if item.qty == row.quantity:
                                # lot.lot_item_details.remove(item)
                                item.delete()
                            else:
                                item.qty -= row.quantity
                                item.save()
                                # End For lot on edit

        if request.company.settings.show_locations:
            # For Location on edit
            for row in obj.rows.all():
                location = row.location
                if location:
                    for item in location.contains.all():
                        if item.item == row.item:
                            if item.qty == row.quantity:
                                # location.contains.remove(item)
                                item.delete()
                            else:
                                item.qty -= row.quantity
                                item.save()
                                # End For Location on edit

    else:
        obj = PurchaseVoucher(company=request.company)
    try:
        obj = save_model(obj, object_values)
        dct['id'] = obj.id
        model = PurchaseVoucherRow
        grand_total = 0

        # if params.get('tax_vm').get('tax') == 'no':
        #     common_tax = True
        #     tax_scheme = None

        for ind, row in enumerate(params.get('table_view').get('rows')):
            if invalid(row, ['item_id', 'quantity', 'rate', 'unit_id']):
                continue
            else:
                if params.get('tax') == 'no' or params.get('tax_scheme_id'):
                    row_tax_scheme_id = None
                else:
                    row_tax_scheme_id = row.get('tax_scheme_id')
                # if request.company.settings.discount_on_voucher:
                #     discount = None
                # else:
                #     discount = row.get('discount')

                item_id = row.get('item')['id']

                if request.company.settings.show_lot:
                    # Setting lot items
                    lot_number = row.get('lot_number')
                    po_receive_lot, created = Lot.objects.get_or_create(
                        lot_number=lot_number
                    )

                    item_exists = False

                    for item in po_receive_lot.lot_item_details.all():
                        if item.item_id == item_id:
                            item_exists = True
                            item.qty += int(row.get('quantity'))
                            item.save()
                    if not item_exists:
                        lot_item_detail = LotItemDetail.objects.create(
                            lot=po_receive_lot,
                            item_id=item_id,
                            qty=int(row.get('quantity'))
                        )
                        # po_receive_lot.lot_item_details.add(lot_item_detail)
                        # End Setting Lot Items
                else:
                    po_receive_lot = None

                if request.company.settings.show_locations:
                    # Setting Location Items
                    item_in_location = False
                    location_id = row.get('location')
                    if location_id:
                        location_obj = Location.objects.get(id=location_id)
                        for item in location_obj.contains.all():
                            if item.item_id == item_id:
                                item_in_location = True
                                item.qty += int(row.get('quantity'))
                                item.save()
                        if not item_in_location:
                            loc_contain_obj = LocationContain.objects.create(
                                location=location_obj,
                                item_id=item_id,
                                qty=int(row.get('quantity'))
                            )
                            # location_obj.contains.add(loc_contain_obj)

                            # End Setting Location Items
                values = {
                    'sn': ind + 1,
                    'item_id': row.get('item')['id'],
                    'quantity': row.get('quantity'),
                    'rate': row.get('rate'),
                    'unit_id': row.get('unit')['id'],
                    'discount': row.get('discount') or 0,
                    'tax_scheme_id': row_tax_scheme_id,
                    'purchase': obj,
                    'lot': po_receive_lot,
                    'location_id': row.get('location')
                    # 'lot_item_detail': lot_item_detail
                }
                submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
                if not created:
                    submodel = save_model(submodel, values)
                grand_total += submodel.get_total()
                dct['rows'][ind] = submodel.id
                set_transactions(submodel, obj.date,
                                 ['dr', submodel.item.account, submodel.quantity],
                                 )

        delete_rows(params.get('table_view').get('deleted_rows'), model)

        if obj.credit:
            cr_acc = obj.party.supplier_account
        else:
            cash_account = get_account(obj.company, 'Cash')
            cr_acc = cash_account

        # Voucher discount needs to broken into row discounts
        if grand_total and obj.discount:
            discount_rate = obj.discount / grand_total
        else:
            discount_rate = None

        try:
            discount_income = Account.objects.get(name='Discount Income', company=obj.company, fy=obj.company.fy,
                                                  category__name='Indirect Income')
        except Account.DoesNotExist:
            discount_income = None

        for purchase_row in obj.rows.all():

            tax_scheme = obj.tax_scheme or purchase_row.tax_scheme

            rate = float(purchase_row.rate)
            row_discount = float(purchase_row.discount) or 0

            if obj.tax == 'inclusive' and tax_scheme:
                rate = rate * 100 / (100 + tax_scheme.percent)
                row_discount = row_discount * 100 / (100 + tax_scheme.percent)

            pure_total = purchase_row.quantity * rate

            divident_discount = 0

            # If the voucher has discount, apply discount proportionally
            if discount_rate:
                if obj.tax == 'inclusive' and tax_scheme:
                    discount_rate = discount_rate * 100 / (100 + tax_scheme.percent)
                divident_discount = (pure_total - row_discount) * discount_rate

            discount = row_discount + divident_discount

            purchase_price = pure_total

            if not discount_income:
                purchase_price -= discount

            entries = [['dr', purchase_row.item.purchase_ledger, purchase_price]]

            if tax_scheme:
                tax_amt = (pure_total - discount) * tax_scheme.percent / 100
                entries.append(['dr', tax_scheme.receivable, tax_amt])
            else:
                tax_amt = 0

            if discount and discount_income:
                entries.append(['cr', discount_income, discount])
            elif discount_income:
                entries.append(['dr', discount_income, 0])

            payable = pure_total - discount + tax_amt

            entries.append(['cr', cr_acc, payable])

            set_ledger_transactions(purchase_row, obj.date, *entries)

        obj.total_amount = grand_total
        if obj.credit:
            # TODO when pending amount exists
            obj.pending_amount = grand_total
        obj.save()
    except Exception as e:
        dct = write_error(dct, e)
        mail_exception(request)
    return JsonResponse(dct)


class SaleCreate(SaleView, CashierMixin, TableObjectMixin):
    template_name = 'sale_form.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SaleCreate, self).get_context_data(**kwargs)
        if not self.kwargs:
            obj = context['obj']
            tax = self.request.company.settings.sale_default_tax_application_type
            tax_scheme = self.request.company.settings.sale_default_tax_scheme
            if tax:
                obj.tax = tax
            if tax_scheme:
                obj.tax_scheme = tax_scheme
            data = self.serializer_class(obj).data
            item_obj = Item.objects.filter(company=self.request.company)
            item_data = ItemSerializer(item_obj, context={'request': self.request, 'voucher': 'sale'}, many=True).data

            context['obj'] = obj
            context['data'] = data
            context['data']['tax'] = get_serialize_data(TaxSchemeSerializer, self.request.company)
            context['data']['items'] = item_data
            context['data']['units'] = get_serialize_data(UnitSerializer, self.request.company)
            context['data']['parties'] = get_serialize_data(PartyBalanceSerializer, self.request.company)

        return context


class SaleDelete(SaleView, CashierMixin, DeleteView):
    pass


# def sale(request, id=None):
#     if id:
#         obj = get_object_or_404(Sale, id=id)
#         scenario = 'Update'
#     else:
#         obj = Sale(date=datetime.datetime.now().date(), company__in=request.company.get_all())
#         scenario = 'Create'
#     data = SaleSerializer(obj).data
#     return render(request, 'sale_form.html', {'data': data, 'scenario': scenario, 'sale': obj})

@group_required('Cashier')
def save_sale(request):
    if request.is_ajax():
        params = json.loads(request.body)
    dct = {'rows': {}, 'tax': {}}
    object_values = {'voucher_no': empty_to_none(params.get('voucher_no')), 'date': params.get('date'),
                     'party_id': params.get('party_id'), 'due_date': params.get('due_date'),
                     'discount': params.get('voucher_discount'),
                     'credit': params.get('credit'), 'tax': params.get('tax'),
                     'tax_scheme_id': empty_to_none(params.get('tax_scheme_id')),
                     'company': request.company}

    if params.get('id'):
        obj = Sale.objects.get(id=params.get('id'), company__in=request.company.get_all())

        if request.company.settings.show_locations:
            # SaleFromLocation Logic here for edit
            for roo in obj.rows.all():
                for sale_frm_loc in roo.from_locations.all():
                    itm_in_loc = sale_frm_loc.location.contains.all().filter(item=roo.item)
                    if itm_in_loc:
                        itm_in_loc[0].qty += sale_frm_loc.qty
                        itm_in_loc[0].save()
                        sale_frm_loc.delete()
                    else:
                        LocationContain.objects.create(
                            location=sale_frm_loc.location,
                            item=roo.item,
                            qty=sale_frm_loc.qty
                        )
                        sale_frm_loc.delete()

                        # End SaleFromLocation Logic here for edit

    else:
        obj = Sale(company=request.company)
    try:
        obj = save_model(obj, object_values)
        dct['id'] = obj.id
        model = SaleRow
        grand_total = 0

        for ind, row in enumerate(params.get('table_view').get('rows')):
            if invalid(row, ['item_id', 'quantity', 'unit_id']):
                continue
            else:
                if params.get('tax') == 'no' or params.get('tax_scheme_id'):
                    row_tax_scheme_id = None
                else:
                    row_tax_scheme_id = row.get('tax_scheme_id')

                values = {'sn': ind + 1, 'item_id': row.get('item')['id'], 'quantity': row.get('quantity'),
                          'rate': row.get('rate'), 'unit_id': row.get('unit')['id'], 'discount': row.get('discount'),
                          'tax_scheme_id': row_tax_scheme_id,
                          'sale': obj}
                submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
                if not created:
                    submodel = save_model(submodel, values)
                # else:
                if request.company.settings.show_locations:
                    # Sale from Location logic here of save
                    item_from_locations = row.get('sale_row_locations')

                    for item in item_from_locations:
                        sale_from_location = SaleFromLocation.objects.create(
                            sale_row=submodel,
                            location_id=int(item.get('location_id')),
                            qty=int(item.get('selected_qty'))
                        )
                        # Deduct item qty from that location or delete
                        location_contain_obj = sale_from_location.location.contains.all().filter(item=submodel.item)[0]
                        if location_contain_obj.qty == sale_from_location.qty:
                            location_contain_obj.delete()
                        else:
                            location_contain_obj.qty -= sale_from_location.qty
                            location_contain_obj.save()
                            # End Deduct item qty from that locatio or delete
                            # End Sale from Location logic here of save

                grand_total += submodel.get_total()
                dct['rows'][ind] = submodel.id
                set_transactions(submodel, obj.date,
                                 ['cr', submodel.item.account, submodel.quantity],
                                 )

        if obj.credit:
            dr_acc = obj.party.customer_account
        else:
            cash_account = get_account(obj.company, 'Cash')
            dr_acc = cash_account

        # Voucher discount needs to broken into row discounts
        if grand_total and obj.discount:
            discount_rate = obj.discount / grand_total
        else:
            discount_rate = None

        try:
            discount_expense = Account.objects.get(name='Discount Expenses', company=obj.company, fy=obj.company.fy,
                                                   category__name='Indirect Expenses')
        except Account.DoesNotExist:
            discount_expense = None

        for sale_row in obj.rows.all():

            tax_scheme = obj.tax_scheme or sale_row.tax_scheme

            rate = float(sale_row.rate)
            row_discount = float(sale_row.discount) or 0

            if obj.tax == 'inclusive' and tax_scheme:
                rate = rate * 100 / (100 + tax_scheme.percent)
                row_discount = row_discount * 100 / (100 + tax_scheme.percent)

            pure_total = sale_row.quantity * rate

            divident_discount = 0

            # If the voucher has discount, apply discount proportionally
            if discount_rate:
                if obj.tax == 'inclusive' and tax_scheme:
                    discount_rate = discount_rate * 100 / (100 + tax_scheme.percent)
                divident_discount = (pure_total - row_discount) * discount_rate

            discount = row_discount + divident_discount

            sale_price = pure_total

            if not discount_expense:
                sale_price -= discount

            entries = [['cr', sale_row.item.sale_ledger, sale_price]]

            if tax_scheme:
                tax_amt = (pure_total - discount) * tax_scheme.percent / 100
                entries.append(['cr', tax_scheme.payable, tax_amt])
            else:
                tax_amt = 0

            if discount and discount_expense:
                entries.append(['dr', discount_expense, discount])
            elif discount_expense:
                entries.append(['dr', discount_expense, 0])

            receivable = pure_total - discount + tax_amt

            entries.append(['dr', dr_acc, receivable])

            set_ledger_transactions(sale_row, obj.date, *entries)
        delete_rows(params.get('table_view').get('deleted_rows'), model)

        if obj.credit:
            # TODO when pending amount exists
            obj.pending_amount = grand_total
        obj.total_amount = grand_total
        obj.save()
    except Exception as e:
        dct = write_error(dct, e)
        mail_exception(request)
    return JsonResponse(dct)


class SaleList(SaleView, CashierMixin, ListView):
    pass


# def sale_list(request):
#     objects = Sale.objects.filter(company__in=request.company.get_all()).prefetch_related('rows')
#     return render(request, 'sale_list.html', {'objects': objects})

@group_required('Cashier')
def sale_day(request, voucher_date):
    objects = Sale.objects.filter(date=voucher_date, company__in=request.company.get_all()).prefetch_related('rows')
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


@group_required('Cashier')
def sale_date_range(request, from_date, to_date):
    objects = Sale.objects.filter(date__gte=from_date, date__lte=to_date, company__in=request.company.get_all()).prefetch_related(
        'rows')
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


@group_required('Cashier')
def sales_report_router(request):
    if request.GET.get('date'):
        return sale_day(request, request.GET.get('date'))
    elif request.GET.get('from') and request.GET.get('to'):
        return sale_date_range(request, request.GET.get('from'), request.GET.get('to'))
    elif request.GET.get('from'):
        return sale_day(request, request.GET.get('from'))
    else:
        return redirect(reverse_lazy('home'))


@group_required('Cashier')
def daily_sale_today(request):
    today = datetime.date.today()
    return sale_day(request, today)


@group_required('Cashier')
def daily_sale_yesterday(request):
    yesterday = datetime.date.today() - datetime.timedelta(1)
    return sale_day(request, yesterday)


class JournalVoucherView(CompanyView):
    model = JournalVoucher
    success_url = reverse_lazy('journal_voucher_list')
    form_class = JournalVoucherForm
    serializer_class = JournalVoucherSerializer
    check = 'can_manage_journal_vouchers'


class JournalVoucherList(JournalVoucherView, AccountantMixin, ListView):
    pass


class JournalVoucherCreate(JournalVoucherView, AccountantMixin, TableObjectMixin):
    template_name = 'voucher/journal_voucher_form.html'

    def get_context_data(self, *args, **kwargs):
        context = super(JournalVoucherCreate, self).get_context_data(**kwargs)
        context['data']['accounts'] = get_serialize_data(AccountSerializer, self.request.company)
        return context


# def journal_voucher_create(request, id=None):
#     if id:
#         journal_voucher = get_object_or_404(JournalVoucher, id=id)
#         scenario = 'Update'
#     else:
#         journal_voucher = JournalVoucher(company=request.company)
#         scenario = 'Create'
#     data = JournalVoucherSerializer(journal_voucher).data
#     return render(request, 'voucher/journal_voucher_form.html', {'data': data, 'scenario': scenario})

@group_required('Accountant')
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
        obj = JournalVoucher.objects.get(id=params.get('id'), company__in=request.company.get_all())
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
                          'description': row.get('description'),
                          'dr_amount': empty_to_none(float(row.get('dr_amount'))),
                          'cr_amount': empty_to_none(float(row.get('cr_amount'))),
                          'journal_voucher': obj}
                submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
                if not created:
                    submodel = save_model(submodel, values)
                dct['rows'][ind] = submodel.id
    except Exception as e:
        dct = write_error(dct, e)
        mail_exception(request)
    delete_rows(params.get('table_view').get('deleted_rows'), model)
    return JsonResponse(dct)


class PurchaseOrderView(CompanyView):
    model = PurchaseOrder
    serializer_class = PurchaseOrderSerializer
    success_url = reverse_lazy("purchase_order_list")
    check = 'can_manage_purchase_orders'


class PurchaseOrderList(PurchaseOrderView, StockistMixin, ListView):
    pass


class PurchaseOrderDelete(PurchaseOrderView, StockistMixin, DeleteView):
    pass


# def purchase_list(request):
#     obj = PurchaseOrder.objects.filter(company__in=request.company.get_all())
#     return render(request, 'purchase_list.html', {'objects': obj})


class PurchaseOrderCreate(PurchaseOrderView, StockistMixin, TableObjectMixin):
    template_name = 'voucher/purchase_order_form.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PurchaseOrderCreate, self).get_context_data(**kwargs)
        item_obj = Item.objects.filter(company=self.request.company)
        item_data = ItemSerializer(item_obj, context={'request': self.request},
                                       many=True).data
        all_ledgers = Account.objects.filter(company=self.request.company, category__name='Purchase Expenses')

        context['data']['items'] = item_data
        context['data']['units'] = get_serialize_data(UnitSerializer, self.request.company)
        context['data']['parties'] = get_serialize_data(PartyBalanceSerializer, self.request.company)
        context['data']['expense_accounts'] = get_serialize_data(AccountSerializer, self.request.company, all_ledgers)
        return context


class PurchaseOrderDetailView(PurchaseOrderView, StockistMixin, DetailView):
    def get_context_data(self, **kwargs):
        context = super(PurchaseOrderDetailView, self).get_context_data(**kwargs)
        context['rows'] = PurchaseOrderRow.objects.select_related('item', 'unit').filter(purchase_order=self.object)
        return context


@group_required('Stockist')
def save_purchase_order(request):
    if request.is_ajax():
        params = json.loads(request.body)
    dct = {'rows': {}, 'expense': {}}
    if params.get('voucher_no') == '':
        params['voucher_no'] = None

    object_values = {'voucher_no': params.get('voucher_no'), 'date': params.get('date'),
                     'party_id': params.get('party_id'), 'purchase_agent_id': params.get('purchase_agent_id'),
                     'company': request.company}

    if params.get('id'):
        obj = PurchaseOrder.objects.get(id=params.get('id'), company__in=request.company.get_all())
    else:
        obj = PurchaseOrder(company=request.company)
    try:
        obj = save_model(obj, object_values)
        dct['id'] = obj.id
        model = PurchaseOrderRow
        # grand_total = 0
        for ind, row in enumerate(params.get('table_view').get('rows')):
            if invalid(row, ['item_id', 'quantity', 'unit_id']):
                continue
            else:
                values = {'sn': ind + 1, 'item_id': row.get('item')['id'], 'specification': row.get('specification'),
                          'quantity': row.get('quantity'),
                          'rate': row.get('rate'), 'unit_id': row.get('unit')['id'], 'remarks': row.get('remarks'),
                          'fulfilled': row.get('fulfilled'),
                          'purchase_order': obj}
                submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
                if not created:
                    submodel = save_model(submodel, values)
                dct['rows'][ind] = submodel.id
        for ind, row in enumerate(params.get('expense_view').get('rows')):
            if invalid(row, ['expense_id', 'amount']):
                continue
            else:
                values = {'expense_id': row.get('expense_id'), 'amount': row.get('amount'),
                          'content_object': obj}
                submodel, created = TradeExpense.objects.get_or_create(id=row.get('id'), defaults=values)
                if not created:
                    submodel = save_model(submodel, values)
                dct['expense'][ind] = submodel.id

        delete_rows(params.get('expense_view').get('deleted_rows'), TradeExpense)

    except Exception as e:
        dct = write_error(dct, e)
        mail_exception(request)
    return JsonResponse(dct)


class CheckifConnected(object):
    def dispatch(self, *args, **kwargs):
        querying_company = self.get_object().company
        if self.request.company.parties.filter(related_company=querying_company):
            return super(CheckifConnected, self).dispatch(*args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('users:party_for_company', kwargs={'company_id': querying_company.id}))


class IncomingPurchaseOrder(CompanyRequiredMixin, StockistMixin, ListView):
    model = PurchaseOrder
    template_name = "voucher/incoming_purchase_order_list.html"
    check = 'can_manage_purchase_orders'

    def get_queryset(self):
        return self.model.objects.filter(party__related_company=self.request.company)


class IncomingPurchaseOrderDetailView(CompanyRequiredMixin, CheckifConnected, StockistMixin, DetailView):
    model = PurchaseOrder
    check = 'can_manage_purchase_orders'

    def get_context_data(self, **kwargs):
        context = super(IncomingPurchaseOrderDetailView, self).get_context_data(**kwargs)
        context['rows'] = PurchaseOrderRow.objects.select_related('item', 'unit').filter(purchase_order=self.object)
        return context


class VoucherSettingUpdateView(SuperOwnerMixin, UpdateView):
    model = VoucherSetting
    form_class = VoucherSettingForm
    success_url = reverse_lazy('home')
    template_name = 'voucher/voucher_setting.html'

    def get_object(self, queryset=None):
        return self.model.objects.get(company=self.request.company)

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Voucher settings updated.')
        return super(VoucherSettingUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(VoucherSettingUpdateView, self).get_context_data(**kwargs)
        context['base_template'] = '_base_settings.html'
        context['setting'] = 'VoucherSetting'
        return context


class ExpenseView(CompanyView):
    model = Expense
    success_url = reverse_lazy('expense_list')
    serializer_class = ExpenseSerializer


class ExpenseList(ExpenseView, AccountantMixin, ListView):
    pass


class ExpenseDelete(ExpenseView, AccountantMixin, DeleteView):
    pass


class ExpenseDetailView(AccountantMixin, DetailView):
    model = Expense

    def get_context_data(self, **kwargs):
        context = super(ExpenseDetailView, self).get_context_data(**kwargs)
        context['rows'] = ExpenseRow.objects.select_related('expense', 'pay_head').filter(expense_row=self.object)
        return context


class ExpenseCreate(ExpenseView, AccountantMixin, TableObjectMixin):
    template_name = 'expense_form.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ExpenseCreate, self).get_context_data(**kwargs)
        all_ledgers = Account.objects.none()
        categories = ['Direct Expenses', 'Indirect Expenses']
        for category_name in categories:
            try:
                category = Category.objects.get(name=category_name, company=self.request.company)
            except Category.MultipleObjectsReturned:
                continue
            ledgers = category.get_descendant_ledgers()
            all_ledgers = all_ledgers | ledgers

        pay_head_categories = ['Bank Account', 'Cash Account']
        pay_head_accounts = Account.objects.filter(company=self.request.company, category__name__in=pay_head_categories)
        context['data']['expense_accounts'] = get_serialize_data(AccountSerializer, self.request.company, all_ledgers)
        context['data']['pay_head_accounts'] = get_serialize_data(AccountSerializer, self.request.company, pay_head_accounts)
        return context

def save_expense(request):
    if request.is_ajax():
        params = json.loads(request.POST.get('expense'))
    company = request.company
    if params.get('voucher_no') == '':
        params['voucher_no'] = None
    dct = {'rows': {}}
    object_values = {'voucher_no': int(params.get('voucher_no')), 'date': params.get('date'),
                     'company': company}
    if params.get('id'):
        obj = Expense.objects.get(id=params.get('id'), company__in=request.company.get_all())
    else:
        obj = Expense(company=request.company)
    try:
        obj = save_model(obj, object_values)
        dct['id'] = obj.id
        model = ExpenseRow
        for ind, row in enumerate(params.get('table_view').get('rows')):
            if invalid(row, ['amount']):
                continue
            values = {'expense_id': row.get('expense_id'),
                      'pay_head_id': row.get('pay_head_id'), 'amount': row.get('amount'),
                      'expense_row': obj}
            submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
            if not created:
                submodel = save_model(submodel, values)
            dct['rows'][ind] = submodel.id
        delete_rows(params.get('table_view').get('deleted_rows'), model)
    except Exception as e:
        mail_exception(request)
        dct = write_error(dct, e)
    return JsonResponse(dct)


def get_item_locations(request, pk=None):
    obj = get_object_or_404(Item, pk=pk)
    data = [{'location_id': loc.location_id, 'location_name': loc.location.name, 'qty': loc.qty} for loc in
            obj.location_contain.all()]
    data = sorted(data, key=lambda dic: dic['location_id'])
    return JsonResponse({'data': data})


def sale_row_onedit_location_item_details(request, sale_row_id=None, item_id=None):
    item = get_object_or_404(Item, pk=item_id)
    sale_row = get_object_or_404(SaleRow, pk=sale_row_id)

    item_present_locations = [{'location_id': loc.location_id, 'location_name': loc.location.name, 'qty': loc.qty} for loc in
                              item.location_contain.all()]
    sale_from_locations = [{'location_id': itm.location_id, 'location_name': itm.location.name, 'selected_qty': itm.qty} for itm
                           in sale_row.from_locations.all()]

    response_data = []
    for dic0 in item_present_locations:
        loc_exists = False
        for dic1 in sale_from_locations:
            if dic0['location_id'] == dic1['location_id']:
                loc_exists = True
                response_data.append(
                    {
                        'location_id': dic0['location_id'],
                        'location_name': dic0['location_name'],
                        'qty': dic0['qty'] + dic1['selected_qty'],
                        'selected_qty': dic1['selected_qty']
                    }
                )
        if not loc_exists:
            response_data.append(
                dic0.copy().update(
                    {
                        'selected_qty': 0
                    }
                )
            )

    for dic0 in sale_from_locations:
        loc_exists = False
        for dic1 in item_present_locations:
            if dic0['location_id'] == dic1['location_id']:
                loc_exists = True
        if not loc_exists:
            response_data.append(
                dic0.copy().update(
                    {
                        'qty': dic0['selected_qty']
                    }
                )
            )
    response_data = sorted(response_data, key=lambda dic: dic['location_id'])
    return JsonResponse({'data': response_data})
