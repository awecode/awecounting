from django.core.urlresolvers import reverse, reverse_lazy
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

from apps.ledger.models import Category, Node
from apps.report.forms import ReportSettingForm
from apps.report.models import ReportSetting
from awecounting.utils.helpers import save_qs_from_ko, get_dict
from awecounting.utils.mixins import group_required, SuperOwnerMixin, UpdateView


def get_trial_balance_data(company):
    root_categories = Category.objects.filter(company=company, parent=None)
    root = {'nodes': [], 'total_dr': 0, 'total_cr': 0, 'settings': model_to_dict(ReportSetting.objects.get(company=company))}
    del root['settings']['id']
    del root['settings']['company']
    for root_category in root_categories:
        node = Node(root_category)
        root['nodes'].append(node.get_data())
        root['total_dr'] += node.dr
        root['total_cr'] += node.cr
    root['settings_save_url'] = reverse('report:save_report_settings')
    return root


@group_required('Accountant')
def trial_balance_json(request):
    return JsonResponse(get_trial_balance_data(request.company))


@group_required('Accountant')
def trial_balance(request):
    data = get_trial_balance_data(request.company)
    context = {
        'data': data,
    }
    return render(request, 'trial_balance.html', context)


@group_required('Accountant')
def save_report_settings(request):
    filter_kwargs = {'company': request.company}
    return JsonResponse(save_qs_from_ko(ReportSetting, filter_kwargs, request.body))


class ReportSettingUpdateView(SuperOwnerMixin, UpdateView):
    model = ReportSetting
    form_class = ReportSettingForm
    success_url = reverse_lazy('home')
    template_name = 'report/report_setting.html'

    def get_object(self, queryset=None):
        return self.model.objects.get(company=self.request.company)

    def get_context_data(self, **kwargs):
        context = super(ReportSettingUpdateView, self).get_context_data(**kwargs)
        context['base_template'] = '_base_settings.html'
        context['setting'] = 'ReportSetting'
        return context


def get_subnode(node, name):
    return get_dict(node['nodes'], 'name', name)

def trading_account(request):
    rows = []
    data = get_trial_balance_data(request.company)
    income = get_subnode(data, 'Income')
    sales = get_subnode(income, 'Sales')
    rows.append(('Sales', sales['cr']))
    expenses = get_subnode(data, 'Expenses')
    purchases = get_subnode(expenses, 'Purchase')
    rows.append(('(Purchases)', purchases['dr']))
    direct_expenses = get_subnode(expenses, 'Direct Expenses')
    rows.append(('(Direct Expenses)', direct_expenses['dr']))
    rows.append(('Gross Profit', float(sales['cr']) - float(purchases['dr'])-float(direct_expenses['dr']), 'ul'))
    return render(request, 'trading_account.html', {'data': data, 'rows': rows})


def profit_loss(request):
    rows = []
    data = get_trial_balance_data(request.company)
    income = get_subnode(data, 'Income')
    sales = get_subnode(income, 'Sales')
    rows.append(('Sales', sales['cr']))
    expenses = get_subnode(data, 'Expenses')
    purchases = get_subnode(expenses, 'Purchase')
    rows.append(('(Purchases)', purchases['dr']))
    direct_expenses = get_subnode(expenses, 'Direct Expenses')
    rows.append(('(Direct Expenses)', direct_expenses['dr']))
    rows.append(('Gross Profit', float(sales['cr']) - float(purchases['dr'])-float(direct_expenses['dr']), 'ul'))
    return render(request, 'profit_loss.html', {'data': data, 'rows': rows})
