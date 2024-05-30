from django_filters.filterset import FilterSet
from .models import Product


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = ['title', 'price', 'discount_price', 'gender']
