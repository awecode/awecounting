from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.views import login
from django.contrib.auth import logout as auth_logout
from allauth.account.forms import LoginForm, SignupForm

from ris.utils.mixins import DeleteView, UpdateView, CreateView
from django.views.generic.list import ListView
from .forms import UserForm, UserUpdateForm
from .models import User
from django.contrib.auth.models import Group


class UserView(object):
    model = User
    success_url = reverse_lazy('user_list')
    form_class = UserForm


class UserDelete(UserView, DeleteView):
    pass


class UserListView(UserView, ListView):
    pass


class UserCreate(UserView, CreateView):
    pass


class UserUpdate(UserView, UpdateView):
    form_class = UserUpdateForm


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
