from django import template
from django import template
from store.models import Cart, Order

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        queryset = Cart.objects.filter(user=user, is_ordered=False).count()
        return queryset
    return 0
    
@register.filter
def cart_total(user):
    if user.is_authenticated:
        queryset = Cart.objects.all().filter(user=user, is_ordered=False)
        return queryset
    
@register.filter
def get_total(user):
    queryset = Order.objects.all().filter(user=user)
    return queryset    
      
    

