import json

from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.generic.detail import DetailView

from awecounting.utils.mixins import DeleteView, UpdateView, CreateView, CompanyView, AjaxableResponseMixin, TableObjectMixin, \
    AccountantMixin, StaffMixin, \
    group_required
from .models import BankAccount, BankCashDeposit, ChequeDeposit, ChequeDepositRow, ChequePayment
from apps.users.models import File as AttachFile
from apps.users.serializers import FileSerializer
from .forms import BankAccountForm, BankCashDepositForm, ChequePaymentForm
from .serializers import ChequeDepositSerializer
from ..ledger.models import delete_rows
from awecounting.utils.helpers import save_model, invalid, write_error


class BankAccountView(CompanyView):
    model = BankAccount
    success_url = reverse_lazy('bank:bankaccount_list')
    form_class = BankAccountForm
    check = 'show_bank_vouchers'


class BankAccountList(BankAccountView, StaffMixin, ListView):
    pass


class BankAccountCreate(AjaxableResponseMixin, AccountantMixin, BankAccountView, CreateView):
    def form_valid(self, form):
        form.instance.company = self.request.company
        return super(BankAccountCreate, self).form_valid(form)


class BankAccountUpdate(BankAccountView, AccountantMixin, UpdateView):
    pass


class BankAccountDelete(BankAccountView, AccountantMixin, DeleteView):
    pass


class CashDepositView(CompanyView):
    model = BankCashDeposit
    success_url = reverse_lazy('bank:cash_deposit_list')
    form_class = BankCashDepositForm
    check = 'show_bank_vouchers'


class CashDepositDelete(CashDepositView, AccountantMixin, DeleteView):
    pass


class CashDepositList(CashDepositView, StaffMixin, ListView):
    pass


class CashDepositCreate(CashDepositView, AccountantMixin, CreateView):
    # def form_valid(self, form):
    # set_transactions(receipt, receipt.date,
    #              ['dr', receipt.bank_account, receipt.amount],
    #              ['cr', receipt.benefactor, receipt.amount],
    #              )
    # return super(BankAccountCreate, self).form_valid(form)
    pass


class CashDepositUpdate(CashDepositView, AccountantMixin, UpdateView):
    pass


class ChequeDepositView(CompanyView):
    model = ChequeDeposit
    success_url = reverse_lazy('bank:cheque_deposit_list')
    serializer_class = ChequeDepositSerializer
    check = 'show_bank_vouchers'


class ChequeDepositList(ChequeDepositView, StaffMixin, ListView):
    pass


class ChequeDepositDetailView(ChequeDepositView, StaffMixin, DetailView):
    pass


class ChequeDepositDelete(ChequeDepositView, AccountantMixin, DeleteView):
    pass


class ChequeDepositCreate(ChequeDepositView, AccountantMixin, TableObjectMixin):
    template_name = 'bank/cheque_deposit_form.html'


# def cheque_deposit_create(request, id=None):
#     if id:
#         cheque_deposit = get_object_or_404(ChequeDeposit, id=id, company=request.company)
#         scenario = 'Update'
#     else:
#         cheque_deposit = ChequeDeposit(company=request.company)
#         scenario = 'Create'

#     return render(request, 'bank/cheque_deposit_form.html',
#                   {'data': ChequeDepositSerializer(cheque_deposit).data, 'scenario': scenario, 'cheque_deposit': cheque_deposit})

@group_required('Accountant')
def cheque_deposit_save(request):
    if request.is_ajax():
        params = json.loads(request.POST.get('cheque_deposit'))
    dct = {'rows': {}}
    company = request.company
    if params.get('voucher_no') == '':
        params['voucher_no'] = None
    object_values = {'voucher_no': int(params.get('voucher_no')), 'date': params.get('date'),
                     'bank_account_id': params.get('bank_account'),
                     'clearing_date': params.get('clearing_date'), 'benefactor_id': params.get('benefactor'),
                     'deposited_by': params.get('deposited_by'),
                     'narration': params.get('narration'), 'status': params.get('status'), 'company': company}
    if params.get('id'):
        obj = ChequeDeposit.objects.get(id=params.get('id'), company=request.company)
    else:
        obj = ChequeDeposit(company=request.company)
    model = ChequeDepositRow
    try:
        obj = save_model(obj, object_values)
        if request.FILES:
            dct['attachment'] = []
            for _file, description in zip(request.FILES.getlist('file'), request.POST.getlist('file_description')):
                attach_file = AttachFile.objects.create(attachment=_file, description=description)
                obj.files.add(attach_file)
                dct['attachment'].append(FileSerializer(attach_file).data)
        if params.get('file'):
            for i, o in enumerate(params.get('file')):
                attach_file_update = get_object_or_404(AttachFile, id=o.get('id'))
                attach_file_update.description = o.get('description')
                attach_file_update.save()
        dct['id'] = obj.id
        for ind, row in enumerate(params.get('table_view').get('rows')):
            if invalid(row, ['cheque_number', 'amount']):
                continue
            else:
                values = {'sn': ind + 1, 'cheque_number': row.get('cheque_number'),
                          'cheque_date': row.get('cheque_date'), 'drawee_bank': row.get('drawee_bank'),
                          'drawee_bank_address': row.get('drawee_bank_address'),
                          'amount': row.get('amount'), 'cheque_deposit': obj}
                submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
                if not created:
                    submodel = save_model(submodel, values)
                dct['rows'][ind] = submodel.id
    except Exception as e:
        dct = write_error(dct, e)
    delete_rows(params.get('table_view').get('deleted_rows'), model)
    delete_rows(params.get('deleted_files'), AttachFile)
    return JsonResponse(dct)


class ChequePaymentView(CompanyView):
    model = ChequePayment
    success_url = reverse_lazy('bank:cheque_payment_list')
    form_class = ChequePaymentForm
    check = 'show_bank_vouchers'


class ChequePaymentList(ChequePaymentView, StaffMixin, ListView):
    pass


class ChequePaymentCreate(ChequePaymentView, AccountantMixin, CreateView):
    pass


class ChequePaymentDelete(ChequePaymentView, AccountantMixin, DeleteView):
    pass


class ChequePaymentUpdate(ChequePaymentView, AccountantMixin, UpdateView):
    pass
