from django.http import JsonResponse
from django.views.generic.edit import UpdateView as BaseUpdateView, CreateView as BaseCreateView, \
    DeleteView as BaseDeleteView, FormView as BaseFormView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required


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
            data = {
                'id': self.object.id
            }
            if hasattr(self.object, 'name'):
                data['name'] = self.object.name
            elif hasattr(self.object, 'title'):
                data['name'] = self.object.title
            else:
                data['name'] = str(self.object)
            return JsonResponse(data)
        else:
            return response
