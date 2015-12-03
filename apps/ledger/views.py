from django.shortcuts import render, get_object_or_404

from apps.ledger.models import Account, JournalEntry


def list_accounts(request):
    objects = Account.objects.filter()
    return render(request, 'list_accounts.html', {'accounts': objects})


def view_account(request, id):
    account = get_object_or_404(Account, id=id)
    # transactions = account.transactions
    base_template = 'dashboard.html'
    journal_entries = JournalEntry.objects.filter(transactions__account_id=account.id).order_by('id',
                                                                                                'date') \
        .prefetch_related('transactions', 'content_type', 'transactions__account').select_related()
    return render(request, 'view_account.html', {
        'account': account,
        # 'transactions': transactions.all(),
        'journal_entries': journal_entries,
        'base_template': base_template,
    })
