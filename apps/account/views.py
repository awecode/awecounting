from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from awecounting.utils.mixins import DeleteView, UpdateView, CreateView, AjaxableResponseMixin
from .models import JournalVoucher, JournalVoucherRow

class JournalVoucherView(object):
	model = JournalVoucher
	success_url = reverse_lazy('account:journalvoucher_list')

class JournalVoucherList(JournalVoucherView, ListView):
	pass


# Create your views here.
