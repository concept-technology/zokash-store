
from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product,Cart, Order, CustomersAddress, Coupon, Category
from django.views.generic import DetailView, ListView,View
from  django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from allauth.account.forms import LoginForm, SignupForm
from django.core.exceptions import ObjectDoesNotExist
from .form import CheckoutForm, CouponForm,RefundRequestForm
from .models import Payment, Refunds
from django.conf import settings
import random
import string



# Create your views here.

def create_ref_code():#generate order reference code
    return ''.join(random.choices(string.ascii_lowercase + string.digits,k=15))


class StoreView(ListView):
    model = Product
    template_name = 'index.html'
    paginate_by= 5
    


def ProductCategories_view(request):
    if request.method == 'GET':
        product = Product.objects.select_related('category').all()
        category = Category.objects.all()
        context= {
            'product':product,
            'category': category
            }
        print(product)
        return render(request, 'store/category.html', context)
    




def category_filter(request, title,):
    if(Category.objects.filter(title=title)):
        product = Product.objects.filter(category__title=title,)
        category = Category.objects.filter(title=title).first()
        context = {'product': product, 'category':category}
        return render(request, 'store/filter.html',context)
    return redirect('store:categories-list')
    
 
@login_required
def dash_board(request):   
  
    cart = Cart.objects.filter(user=request.user, is_ordered=True)
    order = Order.objects.filter(user=request.user, is_ordered=True,)
    
    context = {'order':order, 'cart':cart}
    return render(request, 'store/dashboard.html', context)
       

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

# class ProductCategoriesView(ListView):
#     model = Product
#     paginate_by = 6
#     template_name = 'store/category.html'
    

class CartView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.filter(user=self.request.user, is_ordered=False)
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
                'coupon':CouponForm
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
                billing_address = CustomersAddress.objects.create(user=self.request.user,
                            order=order,                                     
                            street_address=street_address,
                            apartment=apartment, town=town,
                            state=state, country=country,
                            zip_code=zip_code,
                            payment_option=payment_option)              
                order.shipping_address= billing_address
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

        payment = Payment.objects.create(amount=int(amount), email=email,order=order, user=request.user)
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
    
    order = Order.objects.filter(is_ordered= False, user=request.user)[0] 
    payment = Payment.objects.get(ref=ref,)

    if payment.amount == order.get_total():
        payment.verified = True
        payment.save()
        
        order_product = order.product.all()
        order_product.update(is_ordered=True)
        for items in order_product:
            items.save()       
        order.is_ordered = True
        order.Payment = payment
        order.reference = create_ref_code()
        order.save()
        
        
        return render(request, 'store/success.html',)  
    return redirect('')  
    

def get_coupon(request,code):
        try: 
            coupon =  Coupon.objects.get(code=code)
            return coupon         
        except ObjectDoesNotExist:
            messages.error(request, 'coupon does not exist')
            return redirect('store:check-out')

 
def add_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST or None)
        if form.is_valid():
            code =form.cleaned_data.get('code')
            order = Order.objects.get(user=request.user,is_ordered=False,)
            coupon = Coupon.objects.get(code=code, active=True)
            if order.coupon == get_coupon(request, code):
                discount = order.get_total() * coupon.discount / 100
                order.get_total = discount
                order.coupon = coupon
                order.save()
                messages.success(request, 'coupon applied',)
                return redirect('store:check-out')
            messages.error(request, 'ops invalid coupon')
            return redirect('store:check-out')
        return redirect('store:check-out')
    return redirect('store:cart')
                         

class RequestRefund(View):
    
    def get(self, *args, **kwargs):
        form = RefundRequestForm()
        context = {'form': form}
        return render(self.request, 'store/refundpage.html', context)
    
    def post(self, *args, **kwargs):
        form = RefundRequestForm(self.request.POST or None)
        if form.is_valid():
            try:
                reference = form.cleaned_data.get('reference_code')
                message = form.cleaned_data.get('message')
                email = form.cleaned_data.get('email')
                
                order = Order.objects.get(reference= reference)
                order.is_refund_request = True
                order.save()
                
                refund = Refunds()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()
                messages.success(self.request, 'your request is received')
                return redirect('store:index')
            except ObjectDoesNotExist:
                messages.error(self.request, 'invalid order')
                return redirect('store:refund-request')
        messages.error(self.request, 'invalid order')
        return redirect('store:index')
            
