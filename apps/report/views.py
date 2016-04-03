from django.shortcuts import render
from apps.ledger.models import Category


def trial_balance(request):
    categories = Category.objects.filter(company=request.company)
    context = {
        'categories': categories,
    }
    return render(request, 'trial_balance.html', context)
