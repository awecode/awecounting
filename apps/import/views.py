from zipfile import BadZipfile
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from awecounting.utils.helpers import zero_for_none
from ..ledger.models import Party, Account
from ..inventory.models import ItemCategory
from forms import ImportDebtor
from openpyxl import load_workbook

def xls_debtor_tally(row):
    dct = {}
    header = {'A': 'particulars','B': 'debit','C': 'credit'}
    for cell in row:
        dct[header.get(cell.column)] = cell.value
    return dct


def import_debtor_tally(request):
    if request.POST:
        form = ImportDebtor(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            wb = load_workbook(file)
            sheet = wb.worksheets[0]
            rows = tuple(sheet.iter_rows())
            for row in rows[5:]:
                params = xls_debtor_tally(row)
                if type(params.get('debit')) != str and type(params.get('debit')) != str:
                    if 'new_party' in request.POST:
                        party = Party.objects.create(name=params.get('particulars'), company=request.company)
                    else:
                        party, party_created = Party.objects.get_or_create(name=params.get('particulars'), company=request.company)
                    # account = Account.objects.get(name="Opening Balance Difference", category__name="Opening Balance Difference", company=request.company)

                    party.customer_account.opening_cr = zero_for_none(params.get('credit'))
                    # account.opening_dr = zero_for_none(params.get('credit'))

                    party.customer_account.opening_dr = zero_for_none(params.get('debit'))
                    # account.opening_cr = zero_for_none(params.get('debit'))

                    # account.save()
                    party.customer_account.save()
                    party.save()
            return HttpResponseRedirect(reverse('party_list'))
    form = ImportDebtor()
    return render(request, 'import/import_debtor_tally.html', {'form': form})


def import_stock_tally(request):
    if request.POST:
        file = request.FILES['file']
        wb = load_workbook(file)
        sheets = wb.worksheets
        for sheet in sheets:
            category, category_created = ItemCategory.object.get_or_create(name=sheet.title, company=request.company)
    form = ImportDebtor()
    return render(request, 'import/import_debtor_tally.html', {'form': form})

