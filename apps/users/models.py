from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, _user_has_perm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
# from allauth.account.signals import user_logged_in
# from django.dispatch import receiver



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


class StaffOnlyMixin(object):
    def dispatch(self, request, *args, **kwargs):
        u = request.user
        if u.is_authenticated():
            # if bool(u.groups.filter(name__in=group_names)) | u.is_superuser():
            # return True
            if bool(u.groups.filter(name='Staff')):
                return super(StaffOnlyMixin, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied()


# def group_required(*group_names):
#     """Requires user membership in at least one of the groups passed in."""
# 
#     def in_groups(u):
#         if u.is_authenticated():
#             # if bool(u.groups.filter(name__in=group_names)) | u.is_superuser():
#             # return True
#             if bool(u.groups.filter(name__in=group_names)):
#                 return True
#             raise PermissionDenied()
#         return False
# 
#     return user_passes_test(in_groups)


def group_required(*groups):
    def _dec(view_function):

        def _view(request, *args, **kwargs):
            allowed = False
            for role in request.roles:
                if role.group.name in groups:
                    allowed = True
                if allowed:
                    return view_function(request, *args, **kwargs)
                else:
                    if request.user.is_authenticated():
                        raise PermissionDenied()
                    else:
                        return redirect(reverse_lazy('users:login'))

        return _view

    return _dec

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
