from django.shortcuts import render
from .models import Item
# Create your views here.
def index(request):
    context = {'store':Item.objects.all()}
    return render(request, 'index.html', context)
    
def catalogue_item(request, pk=None):
    if pk:
        let_items = Item.objects.get(pk=pk)
    else:
        let_items = ''
    return render(request, 'catalogue.html', {"catalogue": let_items})