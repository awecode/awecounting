from django.db import models
import datetime
from jsonfield import JSONField

class Unit(models.Model):
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=10)

    def __unicode__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=254)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='items', blank=True, null=True)
    size = models.CharField(max_length=250, blank=True, null=True)
    unit = models.ForeignKey(Unit)
    other_properties = JSONField(blank=True, null=True)

    def __unicode__(self):
        return self.name

class Party(models.Model):
    name = models.CharField(max_length=254)
    address = models.CharField(max_length=254, blank=True, null=True)
    phone_no = models.CharField(max_length=100, blank=True, null=True)
    pan_no = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Parties'

class Purchase(models.Model):
    party = models.ForeignKey(Party)
    voucher_no = models.PositiveIntegerField(blank=True, null=True)
    data = models.DateField(default=datetime.datetime.today)

class PurchaseRow(models.Model):
	item = models.ForeignKey(Item)
	quantity = models.FloatField()
	rate = models.FloatField()
	unit = models.ForeignKey(Unit)
	purchase = models.ForeignKey(Purchase, related_name='rows')



