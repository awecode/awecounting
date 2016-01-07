from django.db import models
import datetime
from njango.fields import today, BSDateField
from ..ledger.models import Account
from ..users.models import Company


class ShareHolder(models.Model):
    name = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    company = models.ForeignKey(Company)
    account = models.ForeignKey(Account, null=True)

    def save(self, *args, **kwargs):
        if not self.account_id:
            account = Account(name=self.name, company=self.company)
            account.save()
            self.account = account

        super(ShareHolder, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Collection(models.Model):
    count = models.PositiveIntegerField()
    interest_rate = models.FloatField()
    start_date = BSDateField(blank=True, null=True, default=today)
    end_date = BSDateField(blank=True, null=True, default=today)
    company = models.ForeignKey(Company)

    def __str__(self):
        return str(self.count)

    def get_class_name(self):
        return self.__class__.__name__


class Investment(models.Model):
    share_holder = models.ForeignKey(ShareHolder)
    date = BSDateField(default=today)
    amount = models.FloatField()
    collection = models.ForeignKey(Collection)
    company = models.ForeignKey(Company)

