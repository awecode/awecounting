from django.contrib import admin
from awecounting.utils.mixins import CompanyAdmin
from .models import Entry, EntryRow


class EntryRowInline(admin.TabularInline):
    model = EntryRow


class EntryAdmin(CompanyAdmin):
    inlines = [
        EntryRowInline,
    ]

admin.site.register(Entry, EntryAdmin)
admin.site.register(EntryRow)