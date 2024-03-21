from django.shortcuts import render
from .models import Item
# Create your views here.
def index(request):
    context = {'store':Item.objects.all()}
    return render(request, 'category.html', context)
    
# def index(request):
#     return render(request, 'category.html')