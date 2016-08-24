from django.db import models
from django.dispatch import receiver

from apps.users.models import Company
from apps.users.signals import company_creation


class TrialBalanceReportSetting(models.Model):
    company = models.OneToOneField(Company, related_name='trial_balance_settings')
    show_root_categories_only = models.BooleanField(default=False)
    show_zero_balance_ledgers = models.BooleanField(default=False)
    show_zero_balance_categories = models.BooleanField(default=False)
    show_ledgers_only = models.BooleanField(default=False)

    def __str__(self):
        return 'Trial Balance Settings for ' + str(self.company)


class TradingAccountReportSetting(models.Model):
    company = models.OneToOneField(Company, related_name='trading_account_settings')
    show_root_categories_only = models.BooleanField(default=False)
    show_zero_balance_ledgers = models.BooleanField(default=False)
    show_zero_balance_categories = models.BooleanField(default=False)
    show_ledgers_only = models.BooleanField(default=False)

    def __str__(self):
        return 'Trading Account Settings for ' + str(self.company)


class ProfitAndLossAccountReportSetting(models.Model):
    company = models.OneToOneField(Company, related_name='profit_and_loss_account_settings')
    show_root_categories_only = models.BooleanField(default=False)
    show_zero_balance_ledgers = models.BooleanField(default=False)
    show_zero_balance_categories = models.BooleanField(default=False)
    show_ledgers_only = models.BooleanField(default=False)

    def __str__(self):
        return 'Profit & Loss Settings for ' + str(self.company)


class BalanceSheetReportSetting(models.Model):
    company = models.OneToOneField(Company, related_name='balance_sheet_settings')
    show_root_categories_only = models.BooleanField(default=False)
    show_zero_balance_ledgers = models.BooleanField(default=False)
    show_zero_balance_categories = models.BooleanField(default=False)
    show_ledgers_only = models.BooleanField(default=False)

    def __str__(self):
        return 'Balance Sheet Settings for ' + str(self.company)

class Closing(models.Model):
    company = models.ForeignKey(Company, related_name='closing_account')
    fy = models.PositiveSmallIntegerField(blank=True, null=True)
    inventory_balance = models.FloatField(default=0)
    total_cost = models.FloatField(default=0)

    def __str__(self):
        return str(self.fy) + " : " + str(self.inventory_balance) + " (" + str(self.company) + ")"

    class Meta:
        unique_together = (('company', 'fy'),)

@receiver(company_creation)
def handle_company_creation(sender, **kwargs):
    company = kwargs.get('company')
    TrialBalanceReportSetting.objects.create(company=company)
    TradingAccountReportSetting.objects.create(company=company)
    BalanceSheetReportSetting.objects.create(company=company)
    ProfitAndLossAccountReportSetting.objects.create(company=company)
