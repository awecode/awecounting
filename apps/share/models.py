from django.db import models
import datetime
from apps.users.models import Company


class ShareHolder(models.Model):
    name = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    company = models.ForeignKey(Company)
    
    def __str__(self):
        return self.name

    # TODO
    # Create ledger/account on creation of shareholder


class Collection(models.Model):
    count = models.PositiveIntegerField()
    interest_rate = models.FloatField()
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    company = models.ForeignKey(Company)

    def __str__(self):
        return self.company.name

class Investment(models.Model):
    share_holder = models.ForeignKey(ShareHolder)
    date = models.DateField(default=datetime.date.today)
    amount = models.FloatField()
    collection = models.ForeignKey(Collection)

