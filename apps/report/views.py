import json
from django.http import JsonResponse
from django.shortcuts import render
from apps.ledger.models import Category, Account


class NodeEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super(NodeEncoder, self).__init__(*args, **kwargs)

    def iterencode(self, o, _one_shot=False):
        return 1


def handler(obj):
    print(obj)
    return 1


class Node(object):
    def __init__(self, model, parent=None, depth=0):
        self.children = []
        self.model = model
        self.name = self.model.name
        self.type = self.model.__class__.__name__
        self.dr = 0
        self.cr = 0
        self.depth = depth
        self.parent = parent
        if self.type == 'Category':
            for child in self.model.children.all():
                print self.add_child(Node(child, parent=self, depth=self.depth + 1))
            for account in self.model.accounts.all():
                print self.add_child(Node(account, parent=self, depth=self.depth + 1))
        if self.type == 'Account':
            self.dr = self.model.current_dr or 0
            self.cr = self.model.current_cr or 0
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
            'children': self.children
        }
        return data

    def __str__(self):
        return self.name

def trial_balance(request):
    root_categories = Category.objects.filter(company=request.company, parent=None)
    root = {'items': []}
    for root_category in root_categories:
        node = Node(root_category)
        root['items'].append(node.get_data())
    print(type(root))
    return JsonResponse(root)
    context = {
        'categories': root_categories,
        'root': root,
    }
    return render(request, 'trial_balance.html', context)
