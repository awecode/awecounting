import json
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from awecounting.utils.mixins import CompanyView, DeleteView, SuperOwnerMixin, OwnerMixin, AccountantMixin, StaffMixin, \
    group_required, TableObjectMixin, UpdateView, CreateView, AjaxableResponseMixin
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .models import Entry, EntryRow, Employee, AttendanceVoucher
from .serializers import EntrySerializer
from .forms import EmployeeForm, AttendanceVoucherForm
from awecounting.utils.helpers import save_model, invalid, empty_to_none, delete_rows, zero_for_none, write_error


class EntryView(CompanyView):
    model = Entry
    serializer_class = EntrySerializer


class EntryList(EntryView, ListView):
    pass


class EntryCreate(EntryView, TableObjectMixin):
    template_name = 'payroll/entry_form.html'


class EntryDetailView(EntryView, DetailView):

    def get_context_data(self, **kwargs):
        context = super(EntryDetailView, self).get_context_data(**kwargs)
        context['rows'] = EntryRow.objects.select_related('employee').filter(entry=self.object)
        return context


class EntryDelete(EntryView, DeleteView):
    pass


def save_entry(request):
    if request.is_ajax():
        params = json.loads(request.POST.get('entry'))
    dct = {'rows': {}}
    company = request.company
    if params.get('entry_no') == '':
        params['entry_no'] = None
    object_values = {'entry_no': int(params.get('entry_no')), 'company': company}
    if params.get('id'):
        obj = Entry.objects.get(id=params.get('id'), company=request.company)
    else:
        obj = Entry(company=request.company)
    model = EntryRow
    try:
        obj = save_model(obj, object_values)
        dct['id'] = obj.id
        for ind, row in enumerate(params.get('table_view').get('rows')):
            if invalid(row, ['employee', 'pay_heading']):
                continue
            else:
                values = {'sn': ind + 1, 'employee_id': row.get('employee'),
                          'pay_heading_id': row.get('pay_heading'), 'amount': row.get('amount'),
                          'hours': row.get('hours'), 'tax': row.get('tax'), 'remarks': row.get('remarks'),
                          'entry': obj}
                submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
                if not created:
                    submodel = save_model(submodel, values)
                dct['rows'][ind] = submodel.id
        delete_rows(params.get('table_view').get('deleted_rows'), model)
    except Exception as e:
        dct = write_error(dct, e)
    return JsonResponse(dct)


class EmployeeView(CompanyView):
    model = Employee
    success_url = reverse_lazy('employee_list')
    form_class = EmployeeForm


class EmployeeList(EmployeeView, StaffMixin, ListView):
    pass


class EmployeeCreate(AjaxableResponseMixin, AccountantMixin, EmployeeView, CreateView):
    pass


class EmployeeUpdate(EmployeeView, AccountantMixin, UpdateView):
    pass


class EmployeeDelete(EmployeeView, AccountantMixin, DeleteView):
    pass


class AttendanceVoucherView(CompanyView):
    model = AttendanceVoucher
    success_url = reverse_lazy('attendance_voucher_list')
    form_class = AttendanceVoucherForm


class AttendanceVoucherList(AttendanceVoucherView, StaffMixin, ListView):
    pass


class AttendanceVoucherCreate(AjaxableResponseMixin, AccountantMixin, AttendanceVoucherView, CreateView):
    pass


class AttendanceVoucherUpdate(AttendanceVoucherView, AccountantMixin, UpdateView):
    pass


class AttendanceVoucherDelete(AttendanceVoucherView, AccountantMixin, DeleteView):
    pass
