from django.http import JsonResponse
from django.views.generic.edit import UpdateView as BaseUpdateView, CreateView as BaseCreateView, DeleteView as BaseDeleteView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

from .helpers import json_from_object

from functools import wraps


class DeleteView(BaseDeleteView):
    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = super(DeleteView, self).post(request, *args, **kwargs)
        messages.success(request, ('%s %s' % (self.object.__class__._meta.verbose_name.title(), _('successfully deleted!'))))
        return response


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        return login_required(view)


class UpdateView(BaseUpdateView):
    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['scenario'] = _('Edit')
        context['base_template'] = '_base.html'
        return context


class CreateView(BaseCreateView):
    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['scenario'] = _('Add')
        if self.request.is_ajax():
            base_template = '_modal.html'
        else:
            base_template = '_base.html'
        context['base_template'] = base_template
        return context


class AjaxableResponseMixin(object):
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            return json_from_object(self.object)
        else:
            return response


class CompanyView(object):
    def form_valid(self, form):
        form.instance.company = self.request.company
        return super(CompanyView, self).form_valid(form)

    def get_queryset(self):
        return super(CompanyView, self).get_queryset().filter(company=self.request.company)

    def get_form(self, *args, **kwargs):
        form = super(CompanyView, self).get_form(*args, **kwargs)
        form.company = self.request.company
        if hasattr(form.Meta, 'company_filters'):
            for field in form.Meta.company_filters:
                form.fields[field].queryset = form.fields[field].queryset.filter(company=form.company)
        return form


USURPERS = {
    'Staff': ['Staff', 'Accountant', 'Owner', 'SuperOwner'],
    'Accountant': ['Accountant', 'Owner', 'SuperOwner'],
    'Owner': ['Owner', 'SuperOwner'],
    'SuperOwner': ['SuperOwner'],
}


class StaffMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.role.group.name in USURPERS['Staff']:
                return super(StaffMixin, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied()


class AccountantMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.role.group.name in USURPERS['Accountant']:
                return super(AccountantMixin, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied()


class OwnerMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.role.group.name in USURPERS['Owner']:
                return super(OwnerMixin, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied()


class SuperOwnerMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.role.group.name in USURPERS['SuperOwner']:
                return super(SuperOwnerMixin, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied()


class CompanyAPI(object):
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.filter(company=self.request.company)


class SerializerWithFile(object):
    def get_files(self, obj):
        from apps.users.serializers import FileSerializer

        if obj.pk:
            return FileSerializer(obj.files.all(), many=True).data
        return []


def group_required(group_name):
    def _check_group(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated():
                if request.role.group.name in USURPERS.get(group_name, []):
                    return view_func(request, *args, **kwargs)
            raise PermissionDenied()

        return wrapper

    return _check_group
