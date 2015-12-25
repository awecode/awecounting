from django.core.urlresolvers import reverse_lazy
from awecounting.utils.forms import HTML5BootstrapModelForm
from .models import JournalVoucher, JournalVoucherRow

class JournalVoucherForm(HTML5BootstrapModelForm):
	class Meta:
		model = JournalVoucher
		fields = '__all__'


