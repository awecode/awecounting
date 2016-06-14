from django.shortcuts import render
from forms import ImportDebtor

def import_debtor_tally(request):
    form = ImportDebtor()
    return render(request, 'import/import_debtor_tally.html', {'form': form})
# Create your views here.
