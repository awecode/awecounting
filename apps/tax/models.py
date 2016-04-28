from django.db import models
from django.dispatch import receiver

from ..users.signals import company_creation
from ..ledger.models import Account, Party
from ..users.models import Company


class TaxScheme(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=5, blank=True, null=True)
    percent = models.FloatField()
    recoverable = models.BooleanField(default=False)
    company = models.ForeignKey(Company)

    @property
    def get_name(self):
        if self.name:
            return self.name
        return self.short_name

    def get_class_name(self):
        return self.__class__.__name__

    def save(self, *args, **kwargs):
        if self.pk is None:
            account = Account(name=self.name)
            account.company = self.company
            account.add_category('Duties & Taxes')
            account.save()
            self.account = account
        super(TaxScheme, self).save(*args, **kwargs)

    def __str__(self):
        return self.name + ' (' + str(self.percent) + '%)'


class PartyTaxPreference(models.Model):
    company = models.ForeignKey(Company)
    tax_choices = [('no', 'No Tax'), ('inclusive', 'Tax Inclusive'), ('exclusive', 'Tax Exclusive'),
                   ('no-preference', 'No Preference'), ]
    default_tax_application_type = models.CharField(max_length=15, choices=tax_choices, default='inclusive', null=True,
                                                    blank=True)
    tax_scheme = models.ForeignKey(TaxScheme, blank=True, null=True)
    party = models.OneToOneField(Party, related_name="tax_preference")


@receiver(company_creation)
def handle_company_creation(sender, **kwargs):
    company = kwargs.get('company')
    TaxScheme.objects.create(name="Value Added Tax", short_name='VAT', company=company, percent=13, recoverable=True)
