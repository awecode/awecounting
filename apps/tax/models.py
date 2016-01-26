from django.db import models
from ..users.models import Company


class TaxScheme(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=5, blank=True, null=True)
    percent = models.FloatField()
    recoverable = models.FloatField(default=False)
    company = models.ForeignKey(Company)

    def __str__(self):
        return self.name + ' (' + str(self.percent) + '%)'
