from django.shortcuts import render

from .serializers import ProductSerializer
from  rest_framework import generics
from .models import Product

class ProductView(generics.ListCreateAPIView):
    queryset =  Product
    serializer_class = ProductSerializer
    
