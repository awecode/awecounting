from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.views import login
from django.contrib.auth import logout as auth_logout
# from allauth.account.forms import LoginForm, SignupForm

from awecounting.utils.mixins import DeleteView, UpdateView, CreateView, group_required
from django.views.generic.list import ListView
from .forms import UserForm, UserUpdateForm, RoleForm, CompanyForm, CompanySettingForm, PinForm
from .models import User, Company, Role, CompanySetting, Pin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, JsonResponse
from .serializers import CompanySerializer
from django.views.generic import View
from django.db import IntegrityError


class CompanyPin(ListView):
    model = Company
    template_name = 'company_pin.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyPin, self).get_context_data(**kwargs)
        context['unused_pins'] = self.request.company.pin.filter(used_by__isnull=True)
        context['used_pins'] = self.request.company.pin.filter(used_by__isnull=False)
        if not context['unused_pins']:
            Pin.generate_pin(self.request.company)
            context['unused_pins'] = self.request.company.pin.filter(used_by__isnull=True)
        return context


class AddUserPin(View):
    model = Pin
    form_class = PinForm
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        pin = request.POST.get('code')
        company_id = int(pin.split('-')[0])
        if request.company.id == company_id:
            messages.add_message(request, messages.ERROR, 'Sending request to same company')
            return HttpResponseRedirect(reverse('users:add_user_with_pin'))
        try:
            obj = Pin.objects.get(company_id=company_id, code=pin, used_by__isnull=True)
            obj.used_by = request.company
            obj.save()
            return HttpResponseRedirect(reverse('home'))
        except Pin.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Invalid Pin.')
            return HttpResponseRedirect(reverse('users:add_user_with_pin'))
        except IntegrityError as e:
            messages.add_message(request, messages.ERROR, 'Company already accessible.')
            return HttpResponseRedirect(reverse('users:add_user_with_pin'))


class ValidatePin(View):
    model = Pin

    def get(self, request, *args, **kwargs):
        pin = kwargs.get('pin')
        company = self.model.validate_pin(pin)
        if company is None:
            return JsonResponse({})
        data = CompanySerializer(company).data
        return JsonResponse(data)


class UserView(object):
    model = User
    success_url = reverse_lazy('users:user_list')
    form_class = UserForm


class RoleView(object):
    model = Role
    success_url = reverse_lazy('users:roles')
    form_class = RoleForm


class RoleUpdate(RoleView, UpdateView):
    pass


class UserDelete(UserView, DeleteView):
    pass


class UserListView(UserView, ListView):
    pass


class UserCreate(UserView, CreateView):
    def get_form(self, form_class=None):
        kwargs = self.get_form_kwargs()
        kwargs['request'] = self.request
        return self.form_class(**kwargs)


class UserUpdate(UserView, UpdateView):
    form_class = UserUpdateForm


@login_required
def index(request):
    if request.user.is_authenticated():
        return render(request, 'index.html')
    return login(request)


def web_login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect('/', **kwargs)
    else:
        if request.method == 'POST':
            if 'remember_me' in request.POST:
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)
        return login(request, **kwargs)


def logout(request, next_page=None):
    auth_logout(request)
    if next_page:
        return redirect(next_page)
    return redirect('/')


class GroupView(object):
    model = Group
    fields = '__all__'
    success_url = reverse_lazy('users:group_list')


class GroupListView(GroupView, ListView):
    pass


class GroupCreateView(GroupView, CreateView):
    pass


class GroupUpdateView(GroupView, UpdateView):
    pass


class GroupDeleteView(GroupView, DeleteView):
    pass


class CompanySettingUpdateView(UpdateView):
    model = Company
    form_class = CompanyForm
    secondary_form_class = CompanySettingForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super(CompanySettingUpdateView, self).get_context_data(**kwargs)
        context['secondary_form'] = self.secondary_form_class(instance = self.object.settings, prefix='secondary_form')
        return context

    def post(self, request, **kwargs):
        self.object = self.get_object()
        if request.POST:
            secondary = self.secondary_form_class(request.POST or None, instance=self.object.settings, prefix='secondary_form')
            secondary.company = request.company
            if secondary.is_valid():
                secondary.save()
        return super(CompanySettingUpdateView, self).post(request, **kwargs)


def set_role(request, pk):
    role = Role.objects.get(pk=pk, user=request.user)
    if role:
        request.session['role'] = role.pk
    return redirect(request.META.get('HTTP_REFERER', '/'))


@group_required('Owner')
def roles(request):
    if request.POST:
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError

        try:
            validate_email(request.POST['user'])
            try:
                user = User.objects.get(email=request.POST['user'])
                group = Group.objects.get(name=request.POST['group'])
                try:
                    Role.objects.get(user=user, company=request.company, group=group)
                    messages.error(request,
                                   'User ' + user.username + ' (' + user.email + ') is already the ' + request.POST[
                                       'group'] + '.')
                except Role.DoesNotExist:
                    role = Role(user=user, company=request.company, group=group)
                    role.save()
                    messages.success(request,
                                     'User ' + user.username + ' (' + user.email + ') added as ' + request.POST[
                                         'group'] + '.')
            except User.DoesNotExist:
                messages.error(request, 'No users found with the e-mail address ' + request.POST['user'])
        except ValidationError:
            try:
                user = User.objects.get(username=request.POST['user'])
                group = Group.objects.get(name=request.POST['group'])
                try:
                    Role.objects.get(user=user, company=request.company, group=group)
                    messages.error(request,
                                   'User ' + user.username + ' (' + user.email + ') is already the ' + request.POST[
                                       'group'] + '.')
                except Role.DoesNotExist:
                    role = Role(user=user, company=request.company, group=group)
                    role.save()
                    messages.success(request,
                                     'User ' + user.username + ' (' + user.email + ') added as ' + request.POST[
                                         'group'] + '.')
            except User.DoesNotExist:
                messages.error(request, 'No users found with the username ' + request.POST['user'])
    objs = Role.objects.filter(company=request.company)
    groups = Group.objects.all()
    return render(request, 'roles.html', {'roles': objs, 'groups': groups})


@group_required('Owner')
def delete_role(request, pk):
    obj = Role.objects.get(company=request.company, id=pk)
    if not obj.group.name == 'SuperOwner':
        obj.delete()
        messages.success(request, "%s '%s' %s" % (_('Role'), str(obj), _('successfully deleted.')))
    return redirect(reverse('users:roles'))
