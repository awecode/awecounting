from django.contrib import admin
from apps.tax.models import TaxScheme
from awecounting.utils.mixins import CompanyAdmin

admin.site.register(TaxScheme, CompanyAdmin)
