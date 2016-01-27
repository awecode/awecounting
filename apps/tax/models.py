from django.db import models
from django.dispatch import receiver
from ..users.signals import company_creation
from ..ledger.models import Account
from ..users.models import Company


class TaxScheme(models.Model):
    full_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=5, blank=True, null=True)
    percent = models.FloatField()
    recoverable = models.BooleanField(default=False)
    company = models.ForeignKey(Company)

    @property
    def name(self):
        return self.short_name or self.full_name

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


@receiver(company_creation)
def handle_company_creation(sender, **kwargs):
    company = kwargs.get('company')
    TaxScheme.objects.create(full_name="Value Added Tax", short_name='VAT', company=company, percent=13, recoverable=True)
