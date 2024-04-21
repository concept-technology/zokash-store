from rest_framework import serializers
from .models import Product, Cart, Order
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        

class CartSerializer(serializers.ModelSerializer):
    # ordered_date = serializers.DateField(format="%d-%m-%Y")
    class Meta:
        model = Cart
        fields = '__all__'