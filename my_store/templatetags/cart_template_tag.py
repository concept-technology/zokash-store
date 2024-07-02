from django import template
from django import template
from my_store.models import Cart, Order

register = template.Library()

@register.simple_tag(takes_context=True)
def cart_item_count(context):
    request = context['request']
    if request.user.is_authenticated:
        # Count cart items for authenticated users
        cart_items = Cart.objects.filter(user=request.user, is_ordered=False)
        return cart_items.count()
    else:
        # Count cart items for anonymous users
        cart = request.session.get('cart', {})
        return sum(item['quantity'] for item in cart.values())

    
        
@register.filter
def cart_total(user):
    if user.is_authenticated:
        queryset = Cart.objects.all().filter(user=user, is_ordered=False)
        return queryset
    
@register.filter
def get_total(user):
    queryset = Order.objects.all().filter(user=user)
    return queryset    
      
    

