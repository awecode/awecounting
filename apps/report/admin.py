from django.contrib import admin

from .models import ReportSetting

admin.site.register(ReportSetting)


class ReportSettingStacked(admin.StackedInline):
    model = ReportSetting
