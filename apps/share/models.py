from django.db import models
import datetime


class ShareHolder(models.Model):
    name = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # TODO
    # Create ledger/account on creation of shareholder


class Investment(models.Model):
    share_holder = models.ForeignKey(ShareHolder)
    date = models.DateField(default=datetime.date.today)
    amount = models.FloatField()
