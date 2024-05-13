from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product,Cart, Order
from django.views.generic import DetailView, ListView,View
from  django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from allauth.account.forms import LoginForm, SignupForm
from django.core.exceptions import ObjectDoesNotExist
from .form import CheckoutForm
# Create your views here.
class StoreView(ListView):
    model = Product
    template_name = 'index.html'
    paginate_by= 5
    
class ProductCategoriesView(ListView):
    model = Product
    paginate_by = 5
    template_name = 'store/category.html'
 

def dash_board(request):
    return render(request, 'store/dashboard.html')

class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, 'store/checkout.html', context)
    
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if form.is_valid():
            print(form.cleaned_data, 'form is valid')
            messages.success(self.request, 'please wait while we process your order')
            return(redirect('store:check-out', ))
        messages.error(self.request, 'thre was an error while processing your request')
        return(redirect('store:check-out', ))

def logout_view(request):
    logout(request)
    return redirect('store/index.html')

def register(request):
    form = SignupForm()
    return render(request, 'account/signup.html', {'form': form})


def login(request):
    form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


class HomeView(ListView):
    model = Product
    template_name = 'store/index.html'
    paginate_by= 6
              
class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product.html'

class ProductCategoriesView(ListView):
    model = Product
    paginate_by = 6
    template_name = 'store/category.html'
    

class CartView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.all().filter(user=self.request.user, is_ordered=False)
            cart = Cart.objects.filter(user=self.request.user, is_ordered=False) # filter cart by user
            context = {
                'object':{
                    'cart':cart, 'order':order
                }
            }
            return render(self.request, 'store/cart.html', context )
        except ObjectDoesNotExist:
            messages.error(self.request, 'you dont have an active order')
            return redirect('store:categories')

 



@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart, created = Cart.objects.get_or_create(product=product, user=request.user, is_ordered=False)
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if  order_qs.exists():
        orders =    order_qs[0]
        if orders.product.filter(product__slug=product.slug).exists():
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









@login_required
def delete_cart(request, slug,):
    product = get_object_or_404(Product, slug=slug,)
    cart = Cart.objects.filter(product=product, user=request.user, is_ordered=False)
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if  order_qs.exists():
        orders =    order_qs[0]
        if orders.product.filter(product__slug=product.slug).exists():          
            cart.delete()
            messages.success(request, 'deleted from cart') 
            return redirect('store:cart',)         
        else:
            messages.info(request, 'you have already removed this item from cart')
            return redirect('store:cart')
    else:       
        return redirect('store:categories', slug=slug)
    # return redirect('store:store_item', slug=slug)





 
#increase cart quantity 
@login_required
def increase_cart_quantity(request, slug):
    product = get_object_or_404(Product, slug=slug,)
    cart = Cart.objects.filter(product=product, user=request.user, is_ordered=False)[0]
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if  order_qs.exists():
        orders =    order_qs[0]
        if orders.product.filter(product__slug=product.slug).exists():
            cart.quantity +=1
            cart.save()         
            return redirect('store:cart', )       
        else:
            return redirect('store:cart',)
    else:       
        return redirect('store:cart',)



#reduce cart quantity 
@login_required
def reduce_cart_quantity(request, slug):
    product = get_object_or_404(Product, slug=slug,)
    cart = Cart.objects.filter(product=product, user=request.user, is_ordered=False)[0]
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if  order_qs.exists():
        orders =    order_qs[0]
        if orders.product.filter(product__slug=product.slug).exists():
            cart.quantity -=1
            if cart.quantity >=1:
                cart.save()
            elif cart.quantity ==0:
                cart.delete()      
            return redirect('store:cart')       
        else:
            return redirect('store:cart',)
    else:       
        return redirect('store:cart',)
    # return redirect('store:store_item', slug=slug)
  


    
    
        
        