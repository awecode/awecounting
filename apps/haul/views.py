import re

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from awecounting.tasks import stock_tally, debtor_tally
from forms import ImportFile


def xls_debtor_tally(row):
    dct = {}
    header = {'A': 'particulars', 'B': 'debit', 'C': 'credit'}
    for cell in row:
        dct[header.get(cell.column)] = cell.value
    return dct


def xls_stock_tally(row):
    dct = {}
    header = {'A': 'particulars', 'B': 'quantity', 'C': 'rate', 'D': 'value'}
    for cell in row:
        dct[header.get(cell.column)] = cell.value
        if cell.column == "A":
            data = re.search("\(([^\)]+)\)", cell.value)
            if data:
                dct['oem_number'] = data.group()[1:-1]
    return dct


def import_debtor_tally(request):
    if request.POST:
        form = ImportFile(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            debtor_tally.delay(file, request.company, request.POST)
            return HttpResponseRedirect(reverse('party_list'))
    form = ImportFile()
    return render(request, 'haul/import_debtor_tally.html', {'form': form})


def import_stock_tally(request):
    if request.POST:
        form = ImportFile(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            stock_tally.delay(file, request.company)
            return HttpResponseRedirect(reverse('item_list'))
    form = ImportFile()
    return render(request, 'haul/import_stock_tally.html', {'form': form})
