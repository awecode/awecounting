from django.db import models
from apps.users.models import Company


class ReportSetting(models.Model):
    company = models.OneToOneField(Company, related_name='report_settings')
    # Trial Balance
    show_root_categories_only = models.BooleanField(False)
    show_zero_balance_ledgers = models.BooleanField(False)
    show_zero_balance_categories = models.BooleanField(False)
    hide_all_ledgers = models.BooleanField(False)
    show_ledgers_only = models.BooleanField(False)
