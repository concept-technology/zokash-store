from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product,Cart, Order, BillingAddress
from django.views.generic import DetailView, ListView,View
from  django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from allauth.account.forms import LoginForm, SignupForm
from django.core.exceptions import ObjectDoesNotExist
from .form import CheckoutForm
from .models import Payment
from django.conf import settings


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


# payment view
class PaymentView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'store/paystack.html', {})
        

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
        return redirect('store:categories',)
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
  


# check out view
class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
    
        order = Order.objects.filter(user=self.request.user, is_ordered=False)
        cart= Cart.objects.filter(user=self.request.user, is_ordered=False)
        
        context = {
            'order':{
                'form': form,
                'order': order,
                'cart': cart,
            }
        }
        return render(self.request, 'store/checkout.html', context)


    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        
        try:
            order = Order.objects.get(user=self.request.user, is_ordered=False)
            if form.is_valid():       
                street_address = form.cleaned_data.get('street_address')
                apartment = form.cleaned_data.get('apartment')
                town = form.cleaned_data.get('town')
                state = form.cleaned_data.get('state')
                country = form.cleaned_data.get('country')
                zip_code = form.cleaned_data.get('zip_code')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress.objects.create(user=self.request.user,
                            order=order,                                     
                            street_address=street_address,
                            apartment=apartment, town=town,
                            state=state, country=country,
                            zip_code=zip_code,
                            payment_option=payment_option)              
                order.billing_address= billing_address
                order.save()
                return redirect('store:initiate_payment')
            messages.warning(self.request, 'order failed')
            return(redirect('store:cart', ))
                  
        except ObjectDoesNotExist:
            messages.error(self.request, 'you dont have an active order')
            return redirect('store:categories')




def initiate_payment(request):
    order = Order.objects.get(is_ordered=False, user=request.user)
    cart =Cart.objects.filter(user=request.user, is_ordered=False)
    if request.method == "POST":
        amount = request.POST['amount']
        email = request.POST['email']
        pk = settings.PAYSTACK_PUBLIC_KEY

        payment = Payment.objects.create(amount=int(amount), email=email,order=order)
        payment.save()
        context = {
            'payment': payment,
            'field_values': request.POST,
            'paystack_pub_key': pk,
            'amount_value': payment.amount_value(),
            'order':order         
        }
        
        return render(request, 'store/make-payment.html', context)

    return render(request, 'store/payment.html', {'order':Order.objects.filter(is_ordered=False, user=request.user),'cart':cart})




def verify_payment(request, ref):
    order = Order.objects.get(user=request.user, is_ordered=False)
    payment = Payment.objects.get(ref=ref,order=order)
    verified = payment.verify_payment()
          
    
    if verified:
        payment.order.is_ordered = True
        payment.verified =True       
        payment.save()
        
        return render(request, "store/success.html")
    return redirect('store:initiate_payment')

 
    
        
        