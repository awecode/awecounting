from django.contrib import admin
from awecounting.utils.mixins import CompanyAdmin
from .models import ShareHolder, Collection, Investment

admin.site.register(ShareHolder, CompanyAdmin)
admin.site.register(Collection, CompanyAdmin)
admin.site.register(Investment, CompanyAdmin)
