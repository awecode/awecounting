from django.shortcuts import render
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


def journalvoucher_create(request, pk=None):
	obj = JournalVoucher.objects.get(pk=1)
	data = JournalVoucherSerializer(obj).data
	return render(request, 'account/journalvoucher_form.html')
# Create your views here.
