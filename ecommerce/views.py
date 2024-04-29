from django.shortcuts import render
from django.shortcuts import redirect, render
# from django.views import View
from .models import Product,Cart, Order
from django.views.generic import DetailView, ListView,View
from  django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from allauth.account.forms import LoginForm, SignupForm


# Create your views here.
class StoreView(ListView):
    model = Product
    template_name = 'index.html'
    paginate_by= 5
    
class ProductCategoriesView(ListView):
    model = Product
    paginate_by = 5
    template_name = 'ecommerce/category.html'
 
    
           

class HomeView(ListView):
    model = Product
    template_name = 'ecommerce/index.html'
    paginate_by= 3
              
class ProductDetailView(DetailView):
    model = Product
    template_name = 'ecommerce/product.html'

class ProductCategoriesView(ListView):
    model = Product
    paginate_by = 5
    template_name = 'ecommerce/category.html'

class CartView(View):
    def get(self, *args, **kwargs):
        model = Cart.objects.filter(user=self.request.user, is_ordered=False)
        context = {'cart': model}
        return render(self.request, 'ecommerce/cart.html',context )

    
 
 
 
def logout_view(request):
    logout(request)
    return redirect('ecommerce/index.html')

def register(request):
    form = SignupForm()
    return render(request, 'account/signup.html', {'form': form})


def login(request):
    form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

def add_to_cart(request, slug):
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
        orders = Order.objects.create(user=request.user, is_ordered=False)
        orders.product.add(cart)
        orders.save()

    return redirect('store:store_item',slug=slug,)
        

def delete_cart(request, slug,):
    product = get_object_or_404(Product, slug=slug,)
    cart = Cart.objects.filter(product=product, user=request.user, is_ordered=False)
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if  order_qs.exists():
        orders =    order_qs[0]
        if orders.product.filter(product__slug=product.slug).exists():          
            cart.delete()
            messages.success(request, 'deleted from cart')          
        else:
            messages.info(request, 'you have already removed this item from cart')
            return redirect('store:store_item',slug=slug)
    else:       
        return redirect('store:store_item', slug=slug)
    return redirect('store:store_item', slug=slug)
    
        