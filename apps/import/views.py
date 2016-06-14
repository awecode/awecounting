from django.shortcuts import render
from forms import ImportDebtor
from openpyxl import load_workbook

def import_debtor_tally(request):
    if request.POST:
        form = ImportDebtor(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            wb = load_workbook(file)
            sheet = wb.worksheets[0]
            import ipdb
            ipdb.set_trace()
    form = ImportDebtor()
    return render(request, 'import/import_debtor_tally.html', {'form': form})
# Create your views here.
