from awecounting.utils.forms import HTML5BootstrapModelForm
from models import ReportSetting
from django import forms

class ReportSettingForm(HTML5BootstrapModelForm):
    class Meta:
        model = ReportSetting
        exclude = ('company',)

