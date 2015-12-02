from django.contrib import admin
from .models import ShareHolder, Collection, Investment

admin.site.register(ShareHolder)
admin.site.register(Collection)
admin.site.register(Investment)

# Register your models here.
