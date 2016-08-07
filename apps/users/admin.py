from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, UserChangeForm as DjangoUserChangeForm, \
    UserCreationForm as DjangoUserCreationForm
from django import forms
from django.contrib.admin import ModelAdmin
from django.contrib.sessions.models import Session
from django.core.urlresolvers import reverse

from apps.report.admin import TrialBalanceReportSettingStacked, TradingAccountReportSettingStacked, \
    ProfitAndLossAccountReportSettingStacked, BalanceSheetReportSettingStacked
from awecounting.utils.mixins import CompanyAdmin
from .models import File, User, GroupProxy, Company, Role, Pin, Subscription, Branch


class UserCreationForm(DjangoUserCreationForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta(DjangoUserCreationForm.Meta):
        model = User
        # exclude = ('first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            self._meta.model._default_manager.get(username=username)
        except self._meta.model.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(DjangoUserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    # password = ReadOnlyPasswordHashField(label= ("Password"),
    # help_text= ("Raw passwords are not stored, so there is no way to see "
    # "this user's password, but you can change the password "
    # "using <a href=\"password/\">this form</a>."))

    class Meta(DjangoUserChangeForm.Meta):
        model = User

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    ordering = ('username',)
    filter_horizontal = ()
    list_display = ('username', 'email')
    list_filter = ('is_superuser',)
    fieldsets = ((None,
                  {'fields': ('full_name',
                              'username',
                              'email',
                              'password',
                              'is_superuser',
                              'last_login',
                              )}),
                 )
    add_fieldsets = ((None,
                      {'classes': ('wide',
                                   ),
                       'fields': ('username',
                                  'email',
                                  'password1',
                                  'password2',
                                  'is_superuser')}),
                     )
    search_fields = ('full_name', 'username', 'email', 'devil_no')



admin.site.register(User, CustomUserAdmin)


class GroupAdmin(admin.ModelAdmin):
    # readonly_fields = ['name', ]

    # def has_add_permission(self, request):
    #     return False
    # 
    # def has_delete_permission(self, request, obj=None):
    #     return False
    pass


class FileInline(admin.TabularInline):
    model = File


class SubscriptionStacked(admin.StackedInline):
    model = Subscription


class _CompanyAdmin(ModelAdmin):
    from ..voucher.admin import VoucherSettingStacked

    inlines = [
        VoucherSettingStacked,
        TrialBalanceReportSettingStacked,
        TradingAccountReportSettingStacked,
        ProfitAndLossAccountReportSettingStacked,
        BalanceSheetReportSettingStacked,
        SubscriptionStacked
    ]


from django.contrib.auth.models import Group

admin.site.unregister(Group)
admin.site.register(GroupProxy, GroupAdmin)
admin.site.register(Role, CompanyAdmin)
admin.site.register(Company, _CompanyAdmin)
admin.site.register(File)
admin.site.register(Pin)
admin.site.register(Subscription)
admin.site.register(Branch)


def url_to_edit_object(obj):
    if not obj:
        return 'None'
    url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=(obj.pk,))
    return u'<a href="%s">%s</a>' % (url, obj.__str__())


class SessionAdmin(ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()

    def role(self, obj):
        sess_data = self._session_data(obj)
        try:
            return url_to_edit_object(Role.objects.get(id=sess_data.get('role')))
        except Role.DoesNotExist:
            pass

    role.allow_tags = True

    def user(self, obj):
        sess_data = self._session_data(obj)
        try:
            return url_to_edit_object(User.objects.get(id=sess_data.get('_auth_user_id')))
        except User.DoesNotExist:
            pass

    user.allow_tags = True

    list_display = ['session_key', 'role', 'user', 'expire_date']
    search_fields = ['session_key', ]


admin.site.register(Session, SessionAdmin)
