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
