from awecounting.utils.forms import HTML5BootstrapModelForm
from models import ProfitAndLossAccountReportSetting, TradingAccountReportSetting, \
    TrialBalanceReportSetting, BalanceSheetReportSetting


class TrialBalanceReportSettingForm(HTML5BootstrapModelForm):
    class Meta:
        model = TrialBalanceReportSetting
        exclude = ('company',)


class TradingAccountReportSettingForm(HTML5BootstrapModelForm):
    class Meta:
        model = TradingAccountReportSetting
        exclude = ('company',)


class ProfitAndLossAccountReportSettingForm(HTML5BootstrapModelForm):
    class Meta:
        model = ProfitAndLossAccountReportSetting
        exclude = ('company',)


class BalanceSheetReportSettingForm(HTML5BootstrapModelForm):
    class Meta:
        model = BalanceSheetReportSetting
        exclude = ('company',)
