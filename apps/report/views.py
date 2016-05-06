from django.core.urlresolvers import reverse
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

from apps.ledger.models import Category, Node
from apps.report.models import ReportSetting
from awecounting.utils.helpers import save_qs_from_ko
from awecounting.utils.mixins import group_required


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
