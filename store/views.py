from django.shortcuts import render
from .models import Item
# Create your views here.
def store(request):
    context = {'store':Item.objects.all()}
    return render(request, 'store.html', context)
    
def index(request):
    return render(request, 'index.html')