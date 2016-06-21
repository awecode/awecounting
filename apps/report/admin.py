from django.contrib import admin

from .models import TrialBalanceReportSetting, TradingAccountReportSetting, \
    ProfitAndLossAccountReportSetting, BalanceSheetReportSetting

admin.site.register(TrialBalanceReportSetting)
admin.site.register(TradingAccountReportSetting)
admin.site.register(ProfitAndLossAccountReportSetting)
admin.site.register(BalanceSheetReportSetting)


class TrialBalanceReportSettingStacked(admin.StackedInline):
    model = TrialBalanceReportSetting


class TradingAccountReportSettingStacked(admin.StackedInline):
    model = TradingAccountReportSetting


class ProfitAndLossAccountReportSettingStacked(admin.StackedInline):
    model = ProfitAndLossAccountReportSetting


class BalanceSheetReportSettingStacked(admin.StackedInline):
    model = BalanceSheetReportSetting
