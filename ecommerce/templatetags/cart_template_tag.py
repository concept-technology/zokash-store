from django import template
from django import template
from ecommerce.models import Cart

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        queryset = Cart.objects.filter(user=user, is_ordered=False).count()
        return queryset
    return 0
    
@register.filter
def cart_object(user):
    queryset = Cart.objects.all().filter(user=user)
    return queryset

