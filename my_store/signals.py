import logging

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Cart, Order, Product
import secrets
from django.utils import timezone


logger = logging.getLogger(__name__)

logger.info("signals.py has been imported")


@receiver(user_logged_in)
def transfer_cart_to_user(sender, request, user, **kwargs):
    logger.info("User logged in signal triggered")
    session_cart = request.session.get('cart', {})
    
    if session_cart:
        for item in session_cart.values():
            product = Product.objects.get(id=item['product_id'])
            cart_item, created = Cart.objects.get_or_create(
                user=user,
                product=product,
                defaults={'quantity': item['quantity'], 'is_ordered': False}
            )
            if not created:
                cart_item.quantity += item['quantity']
                cart_item.save()
                
        order, created = Order.objects.get_or_create(
            user=user,
            is_ordered=False,
            defaults={'reference': f'order-{secrets.token_hex(8)}', 'date': timezone.now()}
        )
        
        for item in session_cart.values():
            product = Product.objects.get(id=item['product_id'])
            cart_item = Cart.objects.get(user=user, product=product, is_ordered=False)
            order.product.add(cart_item)
        
        order.save()
        
        del request.session['cart']
        request.session.modified = True
