import copy

from django.core.urlresolvers import reverse, reverse_lazy
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

from apps.ledger.models import Category, Node
from apps.report.forms import ReportSettingForm
from apps.report.models import ReportSetting
from awecounting.utils.helpers import save_qs_from_ko, get_dict
from awecounting.utils.mixins import group_required, SuperOwnerMixin, UpdateView

BALANCE_SHEET = ['Equity', 'Assets', 'Liabilities']
PL_ACCOUNT = ['Income', 'Expenses']


def dict_merge(root, node, combined):
    # Merge only if node with same name exists already in the list of dicts
    if node['name'] in [item.get('name') for item in root]:
        existing_node = get_dict(root, 'name', node['name'])
        # For combined report of branches, Accounts have subnodes of accounts of each branch.
        if combined and node.get('type') == 'Account':
            # Find existing node and make it a subnode
            old_node = copy.deepcopy(existing_node)
            old_node['name'] = old_node['name'] + ' [' + str(old_node['company']) + ']'
            existing_node['nodes'].append(old_node)
            existing_node['url'] = None
            # Create new subnode
            new_node = copy.deepcopy(node)
            new_node['name'] = node['name'] + ' [' + str(node['company']) + ']'
            existing_node['nodes'].append(new_node)
        existing_node['dr'] += node['dr']
        existing_node['cr'] += node['cr']
        if len(node['nodes']):
            for inner_node in node['nodes']:
                dict_merge(existing_node['nodes'], inner_node, combined)
    else:
        root.append(node)
    return root


def get_trial_balance_data(root_company, mode=None, exclude_indirect_accounts=False):
    if root_company.show_combined_reports():
        companies = root_company.get_all()
    else:
        companies = [root_company]
    if len(companies) > 1:
        combined = True
    else:
        combined = False
    root = {'nodes': [], 'total_dr': 0, 'total_cr': 0,
            'settings': model_to_dict(ReportSetting.objects.get(company=root_company), exclude=['id', 'company']),
            'settings_save_url': reverse('report:save_report_settings')}

    for company in companies:
        root_categories = Category.objects.filter(company=company, parent=None)
        if mode:
            root_categories = root_categories.filter(name__in=mode)
        for root_category in root_categories:
            node = Node(root_category)
            root['nodes'] = dict_merge(root['nodes'], node.get_data(), combined)
            root['total_dr'] += node.dr
            root['total_cr'] += node.cr
    root['total_dr'] = round(root['total_dr'], 2)
    root['total_cr'] = round(root['total_cr'], 2)
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


@group_required('Accountant')
def trading_account(request):
    data = get_trial_balance_data(request.company, mode=PL_ACCOUNT)
    context = {
        'data': data,
    }
    return render(request, 'trading_account.html', context)


@group_required('Accountant')
def profit_loss(request):
    data = get_trial_balance_data(request.company, mode=PL_ACCOUNT)
    context = {
        'data': data,
    }
    return render(request, 'profit_loss.html', context)


def dr_bal(node):
    return float(node['dr'] or 0) - (float(node['cr'] or 0))


def cr_bal(node):
    return float(node['cr'] or 0) - (float(node['dr'] or 0))


# def balance_sheet(request):
#     data = get_trial_balance_data(request.company)
#     equity_rows = []
#     liability_rows = []
#     asset_rows = []
# 
#     equity = get_subnode(data, 'Equity')
#     equity_rows.append(('Equity', cr_bal(equity)))
# 
#     liabilities = get_subnode(data, 'Liabilities')
#     payables = get_subnode(liabilities, 'Account Payables')
#     liability_rows.append(('Payables/Suppliers', cr_bal(payables)))
#     taxes = get_subnode(liabilities, 'Duties & Taxes')
#     liability_rows.append(('Duties & Taxes', cr_bal(taxes)))
#     other_payables = get_subnode(liabilities, 'Other Payables')
#     liability_rows.append(('Other Payables', cr_bal(other_payables)))
#     liabilities_total = cr_bal(equity) + cr_bal(payables) + cr_bal(taxes) + cr_bal(other_payables)
# 
#     assets = get_subnode(data, 'Assets')
#     cash_accounts = get_subnode(assets, 'Cash Accounts')
#     asset_rows.append(('Cash in Hand', dr_bal(cash_accounts)))
#     cash_equivalent = get_subnode(assets, 'Cash Equivalent Account')
#     asset_rows.append(('Cash Equivalent', dr_bal(cash_equivalent)))
#     bank_account = get_subnode(assets, 'Bank Account')
#     asset_rows.append(('Bank Accounts', dr_bal(bank_account)))
#     fixed_assets = get_subnode(assets, 'Fixed Assets')
#     asset_rows.append(('Fixed Assets', dr_bal(fixed_assets)))
#     tax_receivables = get_subnode(assets, 'Tax Receivables')
#     asset_rows.append(('Tax Receivables', dr_bal(tax_receivables)))
#     assets_total = dr_bal(cash_accounts) + dr_bal(cash_equivalent) + dr_bal(bank_account) + dr_bal(fixed_assets) + dr_bal(
#         tax_receivables)
# 
#     return render(request, 'balance_sheet.html',
#                   {'data': data, 'equities': equity_rows, 'liabilities': liability_rows, 'assets': asset_rows,
#                    'liabilities_total': liabilities_total, 'assets_total': assets_total})

@group_required('Accountant')
def balance_sheet(request):
    data = get_trial_balance_data(request.company, mode=BALANCE_SHEET)
    context = {
        'data': data,
    }
    return render(request, 'balance_sheet.html', context)