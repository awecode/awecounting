from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.views import login
from django.contrib.auth import logout as auth_logout
# from allauth.account.forms import LoginForm, SignupForm

from awecounting.utils.mixins import DeleteView, UpdateView, CreateView, group_required, CompanyView, SuperOwnerMixin
from django.views.generic.list import ListView
from .forms import UserForm, UserUpdateForm, RoleForm, CompanyForm, PinForm, BranchForm
from .models import User, Company, Role, Pin, Branch
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from .serializers import CompanySerializer
from django.views.generic import View
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from rest_framework import status
from njango.fields import today
from ..ledger.models import Party
from ..ledger.forms import PartyForm


def party_for_company(request, company_id):
    company = Company.objects.get(pk=company_id)
    parties = Party.objects.filter(company=request.company, related_company__isnull=True)
    form = PartyForm(initial={
        'name': company.name,
        'address': company.location,
        'pan_no': company.tax_registration_number
    })
    return render(request, 'party_for_company.html', {'parties': parties, 'company': company, 'form': form})


def set_company_to_party(request, company_id):
    party_id = int(request.POST.get('party_id'))
    party = Party.objects.get(pk=party_id)
    party.related_company_id = int(company_id)
    party.save()
    return HttpResponseRedirect(reverse('home'))


class AccessibleCompanies(ListView):
    model = Pin
    template_name = 'users/accessible_companies.html'

    def get_queryset(self):
        return Pin.accessible_companies(self.request.company)


class ConnectedCompanies(ListView):
    model = Pin
    template_name = 'users/connected_companies.html'

    def get_queryset(self):
        return Pin.connected_companies(self.request.company)


class CompanyPin(ListView):
    model = Company
    template_name = 'company_pin.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyPin, self).get_context_data(**kwargs)
        Pin.generate_pin(self.request.company)
        context['unused_pins'] = self.request.company.pin.filter(used_by__isnull=True)
        context['used_pins'] = self.request.company.pin.filter(used_by__isnull=False)
        return context


class AddUserPin(View):
    model = Pin
    form_class = PinForm
    success_url = reverse_lazy('home')
    template_name = 'users/pin_form.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        pin = request.POST.get('code')
        company_id = int(pin.split('-')[0])
        if request.company.id == company_id:
            messages.add_message(request, messages.ERROR, 'Sending request to same company')
            return HttpResponseRedirect(reverse('users:add_user_with_pin'))
        try:
            obj = Pin.objects.get(company_id=company_id, code=pin, used_by__isnull=True)
            obj.used_by = request.company
            obj.date = today
            obj.save()
            form = PartyForm(initial={
                'name': obj.company.name,
                'address': obj.company.location,
                'pan_no': obj.company.tax_registration_number
            })
            parties = Party.objects.filter(company=request.company, related_company__isnull=True)
            return render(request, 'party_for_company.html', {'parties': parties, 'company': obj.company, 'form': form})
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
        company_id = int(pin.split('-')[0])
        if request.company:
            if request.company.id == company_id:
                return JsonResponse({'Error': 'Sending request to same company'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                company = self.model.validate_pin(pin)
                obj = Pin.objects.get(company_id=company_id, code=pin, used_by__isnull=True)
                obj.used_by = request.company
                obj.save()
                data = CompanySerializer(company).data
                return JsonResponse(data)
            except Pin.DoesNotExist:
                return JsonResponse({'Error': 'Invalid Pin / Pin already used.'}, status=status.HTTP_400_BAD_REQUEST)
            except IntegrityError as e:
                return JsonResponse({'Error': 'Company already accessible.'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'Error': 'Authorization Token required.'}, status=status.HTTP_401_UNAUTHORIZED)


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


class UserDelete(UserView, SuperOwnerMixin, DeleteView):
    pass


class UserListView(UserView, SuperOwnerMixin, ListView):
    def get_queryset(self):
        return super(UserListView, self).get_queryset().filter(roles__company=self.request.company)


class UserCreate(UserView, SuperOwnerMixin, CreateView):
    def get_form(self, form_class=None):
        kwargs = self.get_form_kwargs()
        kwargs['request'] = self.request
        return self.form_class(**kwargs)


class UserUpdate(UserView, SuperOwnerMixin, UpdateView):
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


def demo_login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect('/', **kwargs)
    else:
        if request.method == 'POST':
            if 'remember_me' in request.POST:
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)
        return login(request, template_name='registration/demo_login.html', **kwargs)


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


class CompanySettingUpdateView(SuperOwnerMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        obj = self.request.company
        return obj

    def get_context_data(self, **kwargs):
        context = super(CompanySettingUpdateView, self).get_context_data(**kwargs)
        context['base_template'] = '_base_settings.html'
        context['setting'] = 'Company'
        return context


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


class BranchView(CompanyView):
    model = Branch
    form_class = BranchForm
    success_url = reverse_lazy('users:branch_list')

    def form_valid(self, form):
        super(BranchView, self).form_valid(form)
        self.object = form.instance
        if self.object.is_party and not self.object.party and self.object.branch_company:
            party = Party.objects.get_or_create(name=self.object.name, company=self.request.company,
                                                related_company=self.object.branch_company)
            self.object.party = party
            Role.objects.create(user=self.request.user, group_id=1, company=self.object.branch_company)
        self.object.save()
        return super(BranchView, self).form_valid(form)


class BranchList(BranchView, ListView):
    pass


class BranchCreate(BranchView, CreateView):
    pass


class BranchUpdate(BranchView, UpdateView):
    pass


class BranchDelete(BranchView, DeleteView):
    pass

    #
    #
    # from django.db.models.signals import post_save
    # from django.dispatch import receiver
    #
    # @receiver(post_save, sender=Branch)
    # def branch_save(sender, instance, **kwargs):
    #     import ipdb
    #     ipdb.set_trace()
    #     pass
