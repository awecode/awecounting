import json
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from apps.ledger.models import Category, Account
from apps.report.models import ReportSetting


class Node(object):
    def __init__(self, model, parent=None, depth=0):
        self.children = []
        self.model = model
        self.name = self.model.name
        self.type = self.model.__class__.__name__
        self.dr = 0
        self.cr = 0
        self.url = None
        self.depth = depth
        self.parent = parent
        if self.type == 'Category':
            for child in self.model.children.all():
                self.add_child(Node(child, parent=self, depth=self.depth + 1))
            for account in self.model.accounts.all():
                self.add_child(Node(account, parent=self, depth=self.depth + 1))
        if self.type == 'Account':
            self.dr = self.model.current_dr or 0
            self.cr = self.model.current_cr or 0
            self.url = self.model.get_absolute_url()
        if self.parent:
            self.parent.dr += self.dr
            self.parent.cr += self.cr

    def add_child(self, obj):
        self.children.append(obj.get_data())

    def get_data(self):
        data = {
            'name': self.name,
            'type': self.type,
            'dr': self.dr,
            'cr': self.cr,
            'nodes': self.children,
            'depth': self.depth,
            'url': self.url,
        }
        return data

    def __str__(self):
        return self.name


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
    return root


def trial_balance_json(request):
    return JsonResponse(get_trial_balance_data(request.company))


def trial_balance(request):
    data = get_trial_balance_data(request.company)
    context = {
        'data': data,
    }
    return render(request, 'trial_balance.html', context)
