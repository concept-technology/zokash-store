from .models import ProductsItem, Categories
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = ProductsItem
        

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Categories