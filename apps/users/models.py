from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from njango.fields import BSDateField, today, get_calendar

from njango.nepdate import ad2bs, string_from_tuple, tuple_from_string, bs2ad, bs

import os


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, full_name=''):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            username=username,
            email=UserManager.normalize_email(email),
            full_name=full_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, full_name=''):
        """
        Creates and saves a superuser with the given email, full name and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
            full_name=full_name,
        )
        user.is_superuser = True
        # user.is_staff = True
        user.save(using=self._db)
        return user

    def by_group(self, group_name):
        try:
            group = Group.objects.get(name=group_name)
            return self.filter(groups=group)
        except Group.DoesNotExist:
            return False


class Company(models.Model):
    name = models.CharField(max_length=254)
    location = models.TextField()
    type_of_business = models.CharField(max_length=254)

    def save(self, *args, **kwargs):
        new = False
        if not self.pk:
            new = True
        ret = super(Company, self).save(*args, **kwargs)
        if new:
            from .signals import company_creation

            company_creation.send(sender=None, company=self)
        return ret

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('Companies')


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=245)
    email = models.EmailField(
        verbose_name='email address',
        max_length=254,
        unique=True,
        db_index=True)
    is_superuser = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='users', blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name', 'email']

    def __unicode__(self):
        return self.username

    def get_short_name(self):
        # The user is identified by username
        return self.username

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_perms(self, perm_list, obj=None):
        return self.is_staff

    def email_user(self, subject, context, text_template, html_template=None):
        from django.conf import settings
        from django.core.mail import send_mail
        from django.template.loader import render_to_string

        context['user'] = self
        text_message = render_to_string(text_template, context)
        if html_template:
            html_message = render_to_string(html_template, context)
        else:
            html_message = None

        send_mail(subject, text_message, settings.DEFAULT_FROM_EMAIL, [self.email], fail_silently=False,
                  html_message=html_message)

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def is_admin(self):
        return self.is_superuser

    def get_full_name(self):
        return self.full_name

    def in_group(self, group_name):
        try:
            group = Group.objects.get(name=group_name)
            return group in self.groups.all()
        except Group.DoesNotExist:
            return False

    def add_to_group(self, group_name):
        try:
            group = Group.objects.get(name=group_name)
            self.groups.add(group)
            return True
        except Group.DoesNotExist:
            return False

    objects = UserManager()

    class Meta:
        ordering = ['-id']

    class Meta:
        swappable = 'AUTH_USER_MODEL'


class Role(models.Model):
    user = models.ForeignKey(User, related_name='roles')
    group = models.ForeignKey(Group, related_name='roles')
    company = models.ForeignKey(Company, related_name='roles')

    def __str__(self):
        return str(self.user) + ' as ' + str(self.group) + ' at ' + str(self.company)

    class Meta:
        unique_together = ('user', 'group', 'company')


# def group_required(*groups):
#     def _dec(view_function):
# 
#         def _view(request, *args, **kwargs):
#             allowed = False
#             for role in request.roles:
#                 if role.group.name in groups:
#                     allowed = True
#             if allowed:
#                 return view_function(request, *args, **kwargs)
#             else:
#                 if request.user.is_authenticated():
#                     raise PermissionDenied()
#                 else:
#                     return redirect(reverse_lazy('users:login'))
# 
#         return _view
# 
#     return _dec


class GroupProxy(Group):
    class Meta:
        proxy = True
        verbose_name = _('Group')
        # verbose_name_plural = _('Groups')


# @receiver(user_signed_up)
# @receiver(user_logged_in)
def get_extra_data(request, user, sociallogin=None, **kwargs):
    if sociallogin:
        extra_data = sociallogin.account.extra_data

        if sociallogin.account.provider == 'twitter':
            user.full_name = extra_data['name']

        if sociallogin.account.provider == 'facebook':
            user.full_name = extra_data['name']
            if extra_data['gender'] == 'male':
                user.gender = 'M'
            elif extra_data['gender'] == 'female':
                user.gender = 'F'

        if sociallogin.account.provider == 'google':
            pass
            # user.first_name = sociallogin.account.extra_data['given_name']
            # user.last_name = sociallogin.account.extra_data['family_name']
            # verified = sociallogin.account.extra_data['verified_email']
            # picture_url = sociallogin.account.extra_data['picture']

        user.save()


from django.conf import settings

if 'rest_framework.authtoken' in settings.INSTALLED_APPS:
    from django.db.models.signals import post_save
    from django.dispatch import receiver
    from rest_framework.authtoken.models import Token

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)

    def generate_token():
        for user in User.objects.all():
            Token.objects.get_or_create(user=user)


class CompanySetting(models.Model):
    company = models.OneToOneField(Company, related_name='settings')
    unique_voucher_number = models.BooleanField(default=True)
    use_nepali_fy_system = models.BooleanField(default=True)
    discount_on_voucher = models.BooleanField(default=True)
    voucher_number_start_date = BSDateField(default=today)
    # voucher_number_restart_years = models.IntegerField(default=1)
    # voucher_number_restart_months = models.IntegerField(default=0)
    # voucher_number_restart_days = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # if self.use_nepali_fy_system:
        ret = super(CompanySetting, self).save(*args, **kwargs)
        return ret

    def get_fy_from_date(self, date):
        calendar = get_calendar()
        if type(date) == str or type(date) == unicode:
            date = tuple_from_string(date)
        if calendar == 'ad':
            date = ad2bs(date)
        if type(date) == tuple:
            date = string_from_tuple(date)
        month = int(date.split('-')[1])
        year = int(date.split('-')[0])
        if self.use_nepali_fy_system:
            if month < 4:
                year -= 1
        else:
            day = int(date.split('-')[2])
            if month <= self.voucher_number_start_date.month and day < self.voucher_number_start_date.day:
                year -= 1
        return year

    def get_fy_start(self, date=None):
        year = self.get_fy_from_date(date)
        if self.use_nepali_fy_system:
            fiscal_year_start = str(year) + '-04-01'
        else:
            fiscal_year_start = str(year) + '-' + str(self.voucher_number_start_date.month) + '-' + str(
                self.voucher_number_start_date.day)
        tuple_value = tuple_from_string(fiscal_year_start)
        calendar = get_calendar()
        if calendar == 'ad':
            tuple_value = bs2ad(tuple_value)
        return tuple_value

    def get_fy_end(self, date=None):

        year = self.get_fy_from_date(date)
        if self.use_nepali_fy_system:
            fiscal_year_end = str(int(year) + 1) + '-03-' + str(bs[int(year) + 1][2])
        else:
            # import ipdb
            # ipdb.set_trace()
            fiscal_year_end = str(int(year) + 1) + '-' + str(self.voucher_number_start_date.month) + '-' + str(12)
        tuple_value = tuple_from_string(fiscal_year_end)
        calendar = get_calendar()
        if calendar == 'ad':
            tuple_value = bs2ad(tuple_value)
        return tuple_value

    def __unicode__(self):
        return self.company.name


class File(models.Model):
    attachment = models.FileField(upload_to='cheque_payments/%Y/%m/%d', blank=True, null=True)
    description = models.TextField(max_length=254, null=True, blank=True)

    def filename(self):
        return os.path.basename(self.attachment.name)

    def __str__(self):
        return self.description or self.filename()
