import os
import random

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Group
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from njango.fields import BSDateField, today


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
    ORGANIZATION_TYPES = (
        ('sole_proprietorship', 'Sole Proprietorship'), ('partnership', 'Partnership'), ('corporation', 'Corporation'),
        ('non_profit', 'Non-profit'))
    organization_type = models.CharField(max_length=254, choices=ORGANIZATION_TYPES, default='sole_proprietorship')
    tax_registration_number = models.IntegerField(blank=True, null=True)
    sells_goods = models.BooleanField(default=True)
    sells_services = models.BooleanField(default=False)
    purchases_goods = models.BooleanField(default=True)
    purchases_services = models.BooleanField(default=True)

    def has_shareholders(self):
        return True if self.organization_type in ['partnership', 'corporation'] else False

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


class Subscription(models.Model):
    company = models.ForeignKey(Company)
    enable_purchase = models.BooleanField(default=True)
    enable_purchase_order = models.BooleanField(default=True)
    enable_sales = models.BooleanField(default=True)
    enable_cash_vouchers = models.BooleanField(default=True)
    enable_journal_voucher = models.BooleanField(default=True)
    enable_fixed_assets_voucher = models.BooleanField(default=True)
    enable_bank_vouchers = models.BooleanField(default=True)
    enable_share_management = models.BooleanField(default=True)
    enable_payroll = models.BooleanField(default=True)
    enable_reports = models.BooleanField(default=True)

    def __str__(self):
        return 'Subscription for ' + str(self.company)


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


class File(models.Model):
    attachment = models.FileField(upload_to='cheque_payments/%Y/%m/%d', blank=True, null=True)
    description = models.TextField(max_length=254, null=True, blank=True)

    def filename(self):
        return os.path.basename(self.attachment.name)

    def __str__(self):
        return self.description or self.filename()


class Pin(models.Model):
    code = models.CharField(max_length=100)
    date = BSDateField(blank=True, null=True)
    company = models.ForeignKey(Company, related_name="pin")
    used_by = models.ForeignKey(Company, related_name="used_pin", blank=True, null=True)

    def __str__(self):
        _str = str(self.code) + '-' + self.company.name
        if self.used_by:
            _str += '-' + self.used_by.name
        return _str

    @staticmethod
    def generate_pin(company, count=10):
        pins = Pin.objects.filter(company=company, used_by__isnull=True).count()
        for i in range(pins, count):
            Pin.objects.create(company=company)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(self.company.id) + '-' + str(self.get_code(10000, 99999))
        if self.used_by:
            self.date = today()

        super(Pin, self).save(*args, **kwargs)

    def get_code(self, range_start, range_end):
        if not self.code:
            number_range = range(range_start, range_end)
            code = random.choice(number_range)
            return code

    @staticmethod
    def validate_pin(pin):
        try:
            if not isinstance(pin, str) and not isinstance(pin, unicode):
                return "Set argument in string"
            company_id = int(pin.split('-')[0])
            get_pin = Pin.objects.get(company=company_id, code=pin)
            return get_pin.company
        except Pin.DoesNotExist:
            return None

    @staticmethod
    def companies_list(id):
        return Company.objects.get(pk=id)

    @staticmethod
    def accessible_companies(accessible_by):
        return map(Pin.companies_list, accessible_by.used_pin.all().values_list('company__id', flat=True))

    @staticmethod
    def connected_companies(company):
        return map(Pin.companies_list, company.pin.filter(used_by__isnull=False).values_list('used_by__id', flat=True))

    class Meta:
        unique_together = ("company", "used_by")
