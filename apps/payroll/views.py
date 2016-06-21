import json
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from apps.ledger.models import set_transactions, Account
from awecounting.utils.mixins import CompanyView, DeleteView, SuperOwnerMixin, OwnerMixin, AccountantMixin, StaffMixin, \
    group_required, TableObjectMixin, UpdateView, CreateView, AjaxableResponseMixin
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .models import Entry, EntryRow, Employee
from .serializers import EntrySerializer
from .forms import EmployeeForm
from awecounting.utils.helpers import save_model, invalid, empty_to_none, delete_rows, zero_for_none, write_error, mail_exception


class EntryView(CompanyView):
    model = Entry
    serializer_class = EntrySerializer
    check = 'can_manage_payroll'


class EntryList(EntryView, AccountantMixin, ListView):
    pass


class EntryCreate(EntryView, AccountantMixin, TableObjectMixin):
    template_name = 'payroll/entry_form.html'


class EntryDetailView(EntryView, AccountantMixin, DetailView):
    def get_context_data(self, **kwargs):
        context = super(EntryDetailView, self).get_context_data(**kwargs)
        # TODO Roshan - Why not obj.rows.all in template ?
        context['rows'] = EntryRow.objects.select_related('employee').filter(entry=self.object)
        return context


class EntryDelete(EntryView, AccountantMixin, DeleteView):
    pass


@group_required('Accountant')
def save_entry(request):
    if request.is_ajax():
        params = json.loads(request.POST.get('entry'))
    dct = {'rows': {}}
    company = request.company
    if params.get('entry_no') == '':
        params['entry_no'] = None
    object_values = {'entry_no': int(params.get('entry_no')), 'company': company}
    if params.get('id'):
        obj = Entry.objects.get(id=params.get('id'), company__in=request.company.get_all())
    else:
        obj = Entry(company=request.company)
    model = EntryRow
    try:
        obj = save_model(obj, object_values)
        dct['id'] = obj.id
        for ind, row in enumerate(params.get('table_view').get('rows')):
            if invalid(row, ['employee_id', 'pay_heading_id']):
                continue
            else:
                values = {'sn': ind + 1, 'employee_id': row.get('employee_id'),
                          'pay_heading_id': row.get('pay_heading_id'), 'amount': row.get('amount'),
                          'hours': row.get('hours'), 'tax': row.get('tax'), 'remarks': row.get('remarks'),
                          'entry': obj}
                submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
                if not created:
                    submodel = save_model(submodel, values)
                dct['rows'][ind] = submodel.id
                set_transactions(submodel, obj.created,
                                 ['dr', submodel.pay_heading, submodel.amount],
                                 ['cr', Account.objects.get(name='Payroll Tax', company=obj.company), submodel.tax],
                                 ['cr', submodel.employee, float(submodel.amount) - float(submodel.tax)]
                                 )
        delete_rows(params.get('table_view').get('deleted_rows'), model)
    except Exception as e:
        dct = write_error(dct, e)
        mail_exception(request)
    return JsonResponse(dct)


class EmployeeView(CompanyView):
    model = Employee
    success_url = reverse_lazy('employee_list')
    form_class = EmployeeForm
    check = 'can_manage_payroll'


class EmployeeList(EmployeeView, StaffMixin, ListView):
    pass


class EmployeeCreate(AjaxableResponseMixin, AccountantMixin, EmployeeView, CreateView):
    pass


class EmployeeUpdate(EmployeeView, AccountantMixin, UpdateView):
    pass


class EmployeeDelete(EmployeeView, AccountantMixin, DeleteView):
    pass
