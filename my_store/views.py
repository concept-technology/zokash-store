import secrets
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.views.generic import DetailView, ListView,View
from django.db.models import Q
from  django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from allauth.account.forms import LoginForm, SignupForm
from django.core.exceptions import ObjectDoesNotExist
from .form import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
import random
import string
from django.contrib.sessions.models import Session
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.csrf import csrf_exempt
import logging
from django.template.loader import render_to_string

def create_ref_code():#generate order reference code
    return ''.join(random.choices(string.ascii_lowercase + string.digits,k=15))


class StoreView(ListView):
    model = Product
    template_name = 'index.html'
    paginate_by = 5

    def get_queryset(self):
        return Product.objects.filter(is_best_selling=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['best_selling_products'] = self.get_queryset()
        return context   



from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Product, Category

def ProductCategories_view(request):
    if request.method == 'GET':
        # Get filter parameters from the request
        category_filter = request.GET.get('category')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        size_filter = request.GET.get('size')
        description_filter = request.GET.get('description')

        # Get all products and apply filters
        products = Product.objects.select_related('category').all()

        if category_filter:
            products = products.filter(category__id=category_filter)

        if min_price:
            products = products.filter(price__gte=min_price)

        if max_price:
            products = products.filter(price__lte=max_price)

        if size_filter:
            products = products.filter(size=size_filter)

        if description_filter:
            products = products.filter(description__icontains=description_filter)

        # Get all categories for the filter menu
        categories = Category.objects.all()

        # Implement pagination
        paginator = Paginator(products, 10)  # Show 2 products per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        products_with_ratings = []
        for product in page_obj:
            avg_rating = product.average_rating()
            count = product.ratings.count()
            products_with_ratings.append({'product': product, 'average_rating': avg_rating, 'count': count})

        context = {
            'category': categories,
            'products_with_ratings': products_with_ratings,
            'page_obj': page_obj,
            'selected_category': category_filter,
            'min_price': min_price,
            'max_price': max_price,
            'selected_size': size_filter,
            'description_filter': description_filter,
        }
        return render(request, 'store/category.html', context)



def product_list_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    sizes = Size.objects.all().distinct()  # Get unique sizes

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    size_id = request.GET.get('size')

    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)
    
    if size_id:
        products = products.filter(size__id=size_id)

    products_with_ratings = [
        {
            'product': product,
            'average_rating': product.average_rating()
        }
        for product in products
    ]

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(products_with_ratings, 10)  # Show 10 products per page

    try:
        paginated_products = paginator.page(page)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('store/product_list.html', {'products_with_ratings': paginated_products})
        return JsonResponse({'html': html})

    context = {
        'category': category,
        'products': products,
        'products_with_ratings': paginated_products,
        'min_price': min_price,
        'max_price': max_price,
        'size_id': size_id,
        'sizes': sizes,
        'product_count': products.count(),
    }
    return render(request, 'store/product_list_by_category.html', context)


@login_required
def dash_board(request):   
  
    cart = Cart.objects.filter(user=request.user, is_ordered=True)
    order = Order.objects.filter(user=request.user, is_ordered=True,).order_by('id')
    
    context = {'orders':order, 'cart':cart}
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

 
    

class CartView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            form = CouponForm(self.request.POST)
            delivery = ShippingMethodForm(self.request.POST)
            order = Order.objects.filter(user=self.request.user, is_ordered=False)
            cart = Cart.objects.filter(user=self.request.user, is_ordered=False) # filter cart by user
            coupon = Coupon.objects.filter(active=True)
            context = {
                'coupon': coupon,
                'delivery_form':delivery,
                'coupon_form':form,
                'object':{
                    'cart':cart, 'order':order
                }
            }
            return render(self.request, 'store/cart.html', context )
        except ObjectDoesNotExist:
            messages.error(self.request, 'you dont have an active order')
            return redirect('store:categories')

 

def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.user.is_authenticated:
        cart_qs = Cart.objects.filter(user=request.user, product=product, is_ordered=False)

        if cart_qs.exists():
            cart_item = cart_qs.first()
            cart_item.is_in_cart =True
            cart_item.save()
            messages.success(request, f"Updated {product.title} quantity in cart")
        else:
            cart_item = Cart.objects.create(
                user=request.user,
                product=product,
                quantity=1,
                is_ordered=False
            )
            messages.success(request, f"{product.title} is added to cart")

        # Create or update the order
        order_qs = Order.objects.filter(user=request.user, is_ordered=False)
        if order_qs.exists():
            order = order_qs.first()
        else:
            order = Order.objects.create(
                user=request.user,
                reference=f'order-{secrets.token_hex(8)}',
                date=timezone.now(),
                is_ordered=False
            )

        order.product.add(cart_item)
        order.save()

    else:
        # Handle cart for anonymous users
        cart = request.session.get('cart', {})

        if str(product.id) in cart:
            cart[str(product.id)]['quantity'] += 1
            messages.success(request, f"Updated {product.title} quantity in cart")
        else:
            cart[str(product.id)] = {
                'product_id': product.id,
                'title': product.title,
                'quantity': 1
            }
            messages.success(request, f"{product.title} is added to cart")

        request.session['cart'] = cart

    next_url = request.GET.get('next')
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)

    return redirect("store:index")






def delete_cart(request, slug,):
    product = get_object_or_404(Product, slug=slug,)
    cart = Cart.objects.filter(product=product, user=request.user, is_ordered=False)
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    next_url = request.GET.get('next')
    
    if  order_qs.exists():
        orders =    order_qs[0]
        if orders.product.filter(product__slug=product.slug).exists():          
            cart.delete()
            messages.success(request, 'deleted from cart') 
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect("store:index")        
        else:
            messages.info(request, 'you have already removed this item from cart')
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect("store:index")
    else:
        messages.error(request, 'not deleted')    
        return redirect('store:index',)
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
  
def verify_address(request):
    user = CustomersAddress.objects.all().filter(user=request.user)
    order = Order.objects.filter(user= request.user, is_ordered=False)
    context = {
        'address': user,
        'order': order
     }   
    return render(request, 'store/check-user-address.html', context)    
 


# check out view
class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = AddressForm(self.request.POST or None)
        coupon = Coupon.objects.filter(active=True)

        order = Order.objects.filter(user=self.request.user, is_ordered=False)
        cart= Cart.objects.filter(user=self.request.user, is_ordered=False)
        address =CustomersAddress.objects.filter(user=self.request.user)
        context = {
            'coupon':coupon,
            'order':{
                'form': form,
                'order': order,
                'cart': cart,
                'coupon':CouponForm
            }
        }
        if address.exists():
            return redirect('store:verify-address')
        return render(self.request, 'store/checkout.html', context)
    
    def post(self, *args, **kwargs):
        form = AddressForm(self.request.POST or None)
        
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
                            zip_code=zip_code,)
                            # payment_option=payment_option)              
                order.shipping_address= billing_address
                order.save()
                return redirect('store:initiate_payment')
            messages.warning(self.request, 'order failed')
            return(redirect('store:cart', ))
                  
        except ObjectDoesNotExist:
            messages.error(self.request, 'you dont have an active order')
            return redirect('store:categories')

def Update_addressView(request,pk):
    address = CustomersAddress.objects.get(user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'your address is updated')
            return redirect('store:verify-address')
    else:
        form = AddressForm(instance=address)
    
    context = {
        'form': form,
        'address': address
    }
    return render(request, 'store/update_address.html', context)


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

    return render(request, 'store/payment.html',
                  {'order':Order.objects.filter(is_ordered=False, 
                    user=request.user).order_by('id'),'cart':cart})

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
                return redirect('store:index')
        messages.error(self.request, 'invalid order')
        return redirect('store:index')
 

def apply_coupon(request):
    next_url = request.GET.get('next')  # Define next_url early in the code

    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            try:
                coupon = Coupon.objects.get(code=code, active=True)
                current_time = timezone.now()

                # Check if the coupon is within the validity period
                if coupon.valid_from and coupon.valid_to:
                    if not (coupon.valid_from <= current_time <= coupon.valid_to):
                        messages.warning(request, 'This coupon has expired.')
                        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                            return redirect(next_url)
                        return redirect("store:index")

                # Check if the user has already used this coupon
                if coupon.used_by.filter(id=request.user.id).exists():
                    messages.warning(request, 'You have already used this coupon.')
                    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                        return redirect(next_url)
                    return redirect("store:index")

                order = get_object_or_404(Order, user=request.user, is_ordered=False)
                order.coupon = coupon
                order.save()

                # Mark the coupon as used by this user
                coupon.used_by.add(request.user)
                coupon.save()

                messages.success(request, 'Coupon is applied')
                if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                    return redirect(next_url)
                return redirect("store:index")        
                
            except Coupon.DoesNotExist:
                messages.warning(request, 'This coupon does not exist or is not valid')
                if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                    return redirect(next_url)
                return redirect("store:index")        
                
    else:
        form = CouponForm()
    return render(request, 'store/apply_coupon.html', {'form': form})





class DeliveryUpdate(View):
    def post(self, *args, **kwargs):
        status = self.request.POST.get('confirm')
        order = Order.objects.get(user=self.request.user, is_ordered=True, is_received=False)
        if status:
            order.is_received = True
            order.save()
            messages.success(self.request, 'updated')
            return redirect('store:dash-board')
        messages.error(self.request, 'not updated')
        return redirect('store:dash-board')
        



def select_shipping_method(request):
    if request.method == 'POST':
        form = ShippingMethodForm(request.POST)
        if form.is_valid():
            shipping_method = form.cleaned_data.get('shipping_method')
            order = get_object_or_404(Order, user=request.user, is_ordered=False)
            order.shipping_method = shipping_method
            order.shipping_cost = shipping_method.cost
            order.save()
            messages.success(request, 'Shipping method selected.')
            return redirect('store:order_summary')
    else:
        form = ShippingMethodForm()
    return render(request, 'store/select_shipping_method.html', {'form': form})

def order_summary(request):
    order = get_object_or_404(Order, user=request.user, is_ordered=False)
    context = {
        'order': order,
        'total': order.get_total()
    }
    return render(request, 'store/order_summary.html', context)



def search_view(request):
    query = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    results = Product.objects.all()
    
    if query:
        results = results.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__title__icontains=query)
        )
    
    if min_price:
        try:
            min_price = float(min_price)
            results = results.filter(price__gte=min_price)
        except ValueError:
            pass  # Handle the case where min_price is not a valid number
    
    if max_price:
        try:
            max_price = float(max_price)
            results = results.filter(price__lte=max_price)
        except ValueError:
            pass  # Handle the case where max_price is not a valid number
    
    context = {
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
        'results': results
    }
    
    return render(request, 'store/search_results.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    try:
        is_in_cart = Cart.objects.filter(product=product, is_ordered=False, user=request.user)
    except Cart.DoesNotExist:
        is_in_cart = None

    ratings = product.ratings.all()
    average_rating = product.average_rating()
    user_rating = CustomerRating.objects.filter(user=request.user, product=product).first()
    now = timezone.now()
    all_user_rating = product.ratings.filter(product=product)
    next_product = product.get_next_product()
    related_products = product.get_related_products()  # Fetch related products

    if request.method == 'POST':
        if user_rating:
            rating_form = CustomerRatingForm(request.POST, instance=user_rating)
        else:
            rating_form = CustomerRatingForm(request.POST)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.user = request.user
            rating.product = product
            rating.save()
            return redirect('store:product_detail', slug=product.slug)
    else:
        if user_rating:
            rating_form = None
        else:
            rating_form = CustomerRatingForm()

    context = {
        'user_rating': user_rating,
        'product': product,
        'ratings': ratings,
        'average_rating': average_rating,
        'count': product.ratings.count(),
        'rating_form': rating_form,
        'now': now,
        'all_user_rating': all_user_rating,
        'is_in_cart': is_in_cart,
        'next_product': next_product,
        'related_products': related_products,  # Add related products to context
    }
    return render(request, 'store/product_detail.html', context)

logger = logging.getLogger('django')





class UpdateCartQuantity(View):
    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            id = int(request.POST.get('id'))
            quantity = int(request.POST.get('quantity'))
            size = request.POST.get('size')
            
            product = get_object_or_404(Product, pk=id)
            cart = get_object_or_404(Cart, product=product, is_ordered=False, user=request.user)
            
            cart.quantity = quantity
            if size:
                cart.size = size
            else:
                cart.size = None  # Handle the case where size is not provided
            
            cart.save()
            
            if product.discount_price:
                total_price = product.discount_price * quantity
            else:
                total_price = product.price * quantity
            
            return JsonResponse({
                'product': product.title,
                'id': id,
                'qty': quantity,
                'size': size,  # Ensure to return size even if it's None
                'total_price': total_price
            })
        
        return JsonResponse({'message': 'error'}, status=400)

def mark_order_as_received(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    next_url = request.GET.get('next')  # Define next_url early in the code
    if request.method == 'POST':
        order.is_received = True
        order.is_delivered =True
        order.save()
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            return redirect(next_url)
        return redirect('store:index')       
            # Redirect to the user dashboard or another appropriate page

    return redirect('user-dashboard')
  
def reorder_product(request, product_id):
    pass
#     product = get_object_or_404(Product, id=product_id)
#     cart_item, created = Cart.objects.get_or_create(user=request.user, product=product, is_ordered=False)
#     if not created:
#         cart_item.quantity += 1
#         cart_item.save()
#     return redirect('store:index')                                          
                                            
                                            
def next_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    next_product = product.get_next_product()

    if next_product:
        data = {
            'title': next_product.title,
            'description': next_product.description,
            'price': next_product.price,
            'average_rating': next_product.average_rating(),
            'rating_count': next_product.ratings.count(),
            'slug': next_product.slug,
        }
    else:
        data = {}

    return JsonResponse(data)                                