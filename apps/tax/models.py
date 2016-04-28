from django.db import models
from django.dispatch import receiver

from ..users.signals import company_creation
from ..ledger.models import Account, Party, Category
from ..users.models import Company


class TaxScheme(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=5, blank=True, null=True)
    percent = models.FloatField()
    recoverable = models.BooleanField(default=False)
    ledger = models.ForeignKey(Account, null=True)
    company = models.ForeignKey(Company)

    def save(self, *args, **kwargs):
        super(TaxScheme, self).save(*args, **kwargs)
        if not self.ledger:
            ledger = Account(name=self.name, company=self.company)
            ledger.category = Category.objects.get(name='Duties & Taxes', parent__name='Liabilities', company=self.company)
            ledger.code = 'T-' + str(self.id)
            ledger.save()
            self.ledger = ledger
            self.save()

    @property
    def get_name(self):
        if self.name:
            return self.name
        return self.short_name

    def get_class_name(self):
        return self.__class__.__name__

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
