from django.utils import timezone
from django.shortcuts import redirect, render
from .models import Product, Cart, Order
from django.views.generic import ListView, DetailView
from  django.shortcuts import get_object_or_404
from django.contrib import messages
# Create your views here.
class StoreView(ListView):
    model = Product
    template_name = 'index.html'
    
    
class StoreItemView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    
    
def checkout(request):
    return render(request, 'checkout.html')

def add_to_cart(request, slug,):
    product = get_object_or_404(Product, slug=slug)
    cart, created = Cart.objects.get_or_create(product=product, user=request.user, is_ordered=False)
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if  order_qs.exists():
        orders =    order_qs[0]
        if orders.product.filter(product__slug=product.slug).exists():
            cart.quantity +=1
            messages.info(request,'item added to cart')
            cart.save()
        else:
            orders.product.add(cart)
            messages.info(request,'item updated to cart')
    else: 
        orders = Order.objects.create(user=request.user, is_ordered=False, ordered_date=timezone.now() )
        orders.product.add(cart)
        orders.save()

    return redirect('store:store_item',slug=slug)
        

def delete_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart = Cart.objects.filter(product=product, user=request.user, is_ordered=False)
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if  order_qs.exists():
        orders =    order_qs[0]
        if orders.product.filter(product__slug=product.slug).exists():          
            cart.delete()
            
        else:
            return redirect('store:store_item',slug=slug)
    else:       
        return redirect('store:store_item', slug=slug)
    return redirect('store:store_item', slug=slug)
    
        
        