from django.shortcuts import render
from rest_framework.renderers import TemplateHTMLRenderer
from .serializers import ProductSerializer, ProductCategorySerializer
from  rest_framework import generics
from .models import ProductsItem, Categories


def index(request):
    return render(request, 'ecommerce/product_category.html')

# product display API
class ProductView(generics.ListCreateAPIView):
    queryset =  ProductsItem.objects.all()
    serializer_class = ProductSerializer
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'product_category.html'
 

class ProductSingleItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset =  ProductsItem.objects.all()
    serializer_class = ProductSerializer
    
   

# display product by category API
class ProductCategoryView(generics.ListCreateAPIView):
    queryset =  Categories.objects.all()
    serializer_class = ProductCategorySerializer
    
# display product by single category 
class ProductCategorySingleItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset =  Categories.objects.all()
    serializer_class = ProductCategorySerializer
    
