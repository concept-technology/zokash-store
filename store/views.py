from django.utils import timezone
from django.shortcuts import redirect, render
from .models import Product, Cart, Order
from django.views.generic import ListView, DetailView
from  django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from allauth.account.forms import LoginForm, SignupForm
from django.conf import settings

# Create your views here.
class StoreView(ListView):
    model = Product
    paginate_by = 1 
    template_name = 'index.html'
    
    
class StoreItemView(DetailView):
    model = Product
    template_name = 'product.html'
    
    
def logout_view(request):
    logout(request)
    return redirect('index.html')



def register(request):
    form = SignupForm()
    return render(request, 'account/signup.html', {'form': form})


def login(request):
    form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

def user_profile(request):
    return render(request, 'user_profile.html', {'form':settings.AUTH_USER_MODEL})

def add_to_cart(request, slug,):
    product = get_object_or_404(Product, slug=slug)
    cart, created = Cart.objects.get_or_create(product=product, user=request.user, is_ordered=False)
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if  order_qs.exists():
        orders =    order_qs[0]
        if orders.product.filter(product__slug=product.slug).exists():
            cart.quantity +=1
            cart.save()
            messages.error(request, "This item is already in cart")
        else:
            orders.product.add(cart)
            messages.success(request,f"{product.title} is added to cart ")
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
            messages.success(request, 'deleted from cart')
            
        else:
            messages.info(request, 'no item in cart')
            return redirect('store:store_item',slug=slug)
    else:       
        return redirect('store:store_item', slug=slug)
    return redirect('store:store_item', slug=slug)
    
        
        