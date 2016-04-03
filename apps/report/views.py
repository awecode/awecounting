from django.shortcuts import render
from apps.ledger.models import Category


class Node(object):
    def __init__(self, model, depth=0):
        self.children = []
        self.model = model
        self.name = self.model.name
        self.type = self.model.__class__.__name__
        self.dr = 0
        self.cr = 0
        self.depth = depth
        self.parent = None
        if self.type == 'Category':
            for child in self.model.children.all():
                self.add_child(Node(child, depth=self.depth + 1))
            for account in self.model.accounts.all():
                self.add_child(Node(account, depth=self.depth + 1))

    def add_child(self, obj):
        self.children.append(obj)
        obj.parent = self

    def __str__(self):
        return self.name

    def process_children(self):
        import ipdb

        ipdb.set_trace()


def trial_balance(request):
    root_categories = Category.objects.filter(company=request.company, parent=None)
    root = []
    for root_category in root_categories:
        node = Node(root_category)
        root.append(node)
    import ipdb

    ipdb.set_trace()
    context = {
        'categories': root_categories,
        'root': root,
    }
    return render(request, 'trial_balance.html', context)
