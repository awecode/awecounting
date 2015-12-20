from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from awecounting.utils.mixins import DeleteView, UpdateView, CreateView, AjaxableResponseMixin
from .models import JournalVoucher, JournalVoucherRow
from .forms import JournalVoucherForm
from .serializer import JournalVoucherSerializer, JournalVoucherRowSerializer

class JournalVoucherView(object):
	model = JournalVoucher
	success_url = reverse_lazy('account:journalvoucher_list')
	form_class = JournalVoucherForm

class JournalVoucherList(JournalVoucherView, ListView):
	pass


class JournalVoucherCreate(JournalVoucherView, CreateView):
	pass


def journalvoucher_create(request, id=None):
    if id:
        journal_voucher = get_object_or_404(JournalVoucher, id=id)
        scenario = 'Update'
    else:
        journal_voucher = JournalVoucher(company=request.company)
        scenario = 'Create'
    data = JournalVoucherSerializer(journal_voucher).data
    return render(request, 'account/journalvoucher_form.html', {'data': data})
# Create your views here.
