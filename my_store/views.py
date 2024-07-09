import requests
import secrets
import uuid
from django.http import JsonResponse, HttpResponse
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
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.csrf import csrf_exempt
import logging
from django.template.loader import render_to_string
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import random
# views.py
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
# apps.py
from django.apps import AppConfig
from django.contrib import messages 
from django.contrib.messages import get_messages

def get_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


class MyStoreConfig(AppConfig):
    name = 'my_store'

    def ready(self):
        import my_store.signals

# next_url = request.GET.get('next')  # Define next_url early in the code
#     messages.success(request, 'Coupon is applied')
#                 if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
#                     return redirect(next_url)
class DashBoardView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        
        profile_form = UserProfileForm(instance=self.request.user)
        password_form = PasswordChangeForm(self.request.user)
        cart = Cart.objects.filter(user=self.request.user, is_ordered=True)
        order = Order.objects.filter(user=self.request.user, is_ordered=True).order_by('id')
        
        # Handle case where address might not exist
        address = CustomersAddress.objects.filter(user=self.request.user).first()
        address_form = AddressForm(instance=address) if address else AddressForm()
        
        context = {
            'profile_form': profile_form,
            'password_form': password_form,
            'orders': order,
            'cart': cart,
            'address': address,
            'address_form': address_form,
        }
        return render(self.request, 'store/dashboard.html', context)
    
    def post(self, request, *args, **kwargs):
        profile_form = UserProfileForm(self.request.POST, instance=self.request.user)
        password_form = PasswordChangeForm(self.request.user, self.request.POST)
        
        # Handle case where address might not exist
        address = CustomersAddress.objects.filter(user=self.request.user).first()
        address_form = AddressForm(self.request.POST, instance=address) if address else AddressForm(self.request.POST)
        
        if 'update_profile' in self.request.POST and profile_form.is_valid():
            profile_form.save()
            messages.success(self.request, 'Your profile has been updated successfully!')
            return redirect('store:dash-board')
        
        elif 'change_password' in self.request.POST and password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(self.request, user)  # Important!
            messages.success(self.request, 'Your password has been changed successfully!')
            return redirect('store:dash-board')
        
        elif 'update_address' in self.request.POST and address_form.is_valid():
            address_form.save(commit=False)
            address_form.instance.user = self.request.user  # Ensure the address is linked to the current user
            address_form.save()
            messages.success(self.request, 'Your address has been updated successfully!')
            return redirect('store:dash-board')
        
        # Handle invalid forms
        if not profile_form.is_valid():
            messages.error(self.request, 'There was an error updating your profile.')
        if not password_form.is_valid():
            messages.error(self.request, 'There was an error changing your password.')
        if not address_form.is_valid():
            messages.error(self.request, 'There was an error updating your address.')

        # Re-render the page with the forms and error messages
        context = {
            'profile_form': profile_form,
            'password_form': password_form,
            'orders': Order.objects.filter(user=self.request.user, is_ordered=True).order_by('id'),
            'cart': Cart.objects.filter(user=self.request.user, is_ordered=True),
            'address': address,
            'address_form': address_form,
        }
        return render(self.request, 'store/dashboard.html', context)
   
    





def generate_random_number(digits=10):
    if digits > 10:
        raise ValueError("The number of digits should not exceed 10")
    if digits < 1:
        raise ValueError("The number of digits should be at least 1")
        
    lower_bound = 10**(digits - 1)
    upper_bound = 10**digits - 1
    
    return random.randint(lower_bound, upper_bound)

def create_ref_code():#generate order reference code
    return ''.join(random.choices(string.ascii_lowercase + string.digits,k=15))


class StoreView(ListView):
    model = Product
    template_name = 'index.html'
    paginate_by = 10

    def get_queryset(self):
        return Product.objects.filter(is_best_selling=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['best_selling_products'] = self.get_queryset()
        return context   


def contact_view(request):
    return render(request, 'store/contact.html')


def ProductCategories_view(request):
    if request.method == 'GET':
        # Get filter parameters from the request
        category_filter = request.GET.get('category')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        size_filter = request.GET.get('size')
        description_filter = request.GET.get('description')

        # Get all products and apply filters
        products = Product.objects.select_related('category').all().order_by('id')  # Order the QuerySet by 'id'

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
        categories = Category.objects.all().order_by('title')

        # Implement pagination
        paginator = Paginator(products, 10)  # Show 10 products per page
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
    try:
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=category).order_by('id')  # Order the QuerySet by 'id'
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
    except ObjectDoesNotExist:
        messages.error(request, 'not found on the server')
        return redirect('store:index')
     

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

def get_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

logger = logging.getLogger(__name__)

class CartView(View):
    def get(self, request, *args, **kwargs):
        try:
            coupon_form = CouponForm()
            location_form = AbujaLocationForm()

            if request.user.is_authenticated:
                cart_items = Cart.objects.filter(user=request.user, is_ordered=False)
                order = Order.objects.filter(user=request.user, is_ordered=False).first()
            else:
                session_cart_id = request.session.get('cart_id')
                if not session_cart_id:
                    session_cart_id = str(uuid.uuid4())
                    request.session['cart_id'] = session_cart_id
                    print(f"New session cart_id created: {session_cart_id}")

                cart_items = Cart.objects.filter(cart_id=session_cart_id, is_ordered=False)
                order = Order.objects.filter(cart_id=session_cart_id, is_ordered=False).first()
                
                print(f"Session cart_id: {session_cart_id}")
                print(f"Cart items: {cart_items}")
                print(f"Order: {order}")

            coupons = Coupon.objects.filter(active=True)
            locations = AbujaLocation.objects.all()

            context = {
                'coupon_form': coupon_form,
                'location_form': location_form,
                'locations': locations,
                'coupons': coupons,
                'order': order,
                'cart_items': cart_items,
                'total_with_delivery': order.get_total_with_delivery() if order else 0,
            }

            return render(request, 'store/cart.html', context)

        except ObjectDoesNotExist:
            messages.error(request, 'You do not have an active order.')
            return redirect('store:categories')
    def post(self, request, *args, **kwargs):
        try:
            if request.user.is_authenticated:
                order = Order.objects.filter(user=request.user, is_ordered=False).first()
            else:
                session_cart_id = request.session.get('cart_id')
                if not session_cart_id:
                    session_cart_id = str(uuid.uuid4())
                    request.session['cart_id'] = session_cart_id
                    request.session.modified = True

                order = Order.objects.filter(cart_id=session_cart_id, is_ordered=False).first()

            # Debugging information
            print(f"Order before forms: {order}")

            coupon_form = CouponForm(request.POST)
            location_form = AbujaLocationForm(request.POST)

            if coupon_form.is_valid():
                coupon_code = coupon_form.cleaned_data['code']
                try:
                    coupon = Coupon.objects.get(code=coupon_code, active=True)
                    order.coupon = coupon
                    order.save()
                    messages.success(request, 'Coupon applied successfully.')
                except Coupon.DoesNotExist:
                    messages.error(request, 'Invalid coupon code.')

            if location_form.is_valid():
                location_id = location_form.cleaned_data['location']
                print(f"Location ID from form: {location_id}")
                abuja_location = AbujaLocation.objects.get(id=location_id)
                order.abuja_location = abuja_location
                order.save()
                messages.success(request, 'Delivery location updated successfully.')

            # Debugging information
            print(f"Order after forms: {order}")

            if request.user.is_authenticated:
                cart_items = Cart.objects.filter(user=request.user, is_ordered=False)
            else:
                cart_items = Cart.objects.filter(cart_id=session_cart_id, is_ordered=False)

            coupons = Coupon.objects.filter(active=True)
            locations = AbujaLocation.objects.all()

            context = {
                'coupon_form': coupon_form,
                'location_form': location_form,
                'locations': locations,
                'coupons': coupons,
                'order': order,
                'cart_items': cart_items,
                'total_with_delivery': order.get_total_with_delivery() if order else 0,
            }

            return render(request, 'store/cart.html', context)

        except ObjectDoesNotExist:
            messages.error(request, 'You do not have an active order.')
            return redirect('store:cart')






def cart_count_view(request):
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user, is_ordered=False).count()
    else:
        session_cart_id = request.session.get('cart_id', None)
        if session_cart_id:
            cart_count = Cart.objects.filter(cart_id=session_cart_id, is_ordered=False).count()
        else:
            cart_count = 0
    return JsonResponse({'cart_count': cart_count})


logger = logging.getLogger(__name__)

@csrf_exempt
@require_POST
def add_to_cart(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        slug = request.POST.get('slug')
        product = get_object_or_404(Product, slug=slug)
        quantity = int(request.POST.get('quantity', 1))  # Default quantity to 1 if not provided

        if request.user.is_authenticated:
            cart_qs = Cart.objects.filter(user=request.user, product=product, is_ordered=False)

            if cart_qs.exists():
                cart_item = cart_qs.first()
                cart_item.quantity += quantity  # Update the quantity
                cart_item.save()
                messages.success(request, f"{product.title} quantity updated in cart")
            else:
                cart_item = Cart.objects.create(
                    user=request.user,
                    product=product,
                    quantity=quantity,
                    is_ordered=False
                )
                messages.success(request, f"{product.title} is added to cart")

            # Create or update the order
            order, created = Order.objects.get_or_create(
                user=request.user,
                is_ordered=False,
                defaults={
                    'reference': f'order-{secrets.token_hex(8)}',
                    'date': timezone.now()
                }
            )

            if not order.product.filter(id=cart_item.id).exists():
                order.product.add(cart_item)
            order.save()

            Wishlist.objects.filter(user=request.user, product=product).delete()

            storage = get_messages(request)
            response_messages = [{'message': message.message, 'tags': message.tags} for message in storage]

            cart_count = Cart.objects.filter(user=request.user, is_ordered=False).count()

            return JsonResponse({'success': True, 'cart_count': cart_count, 'messages': response_messages})
        else:
            session_cart_id = request.session.get('cart_id')
            if not session_cart_id:
                session_cart_id = str(uuid.uuid4())
                request.session['cart_id'] = session_cart_id
                request.session.modified = True
                logger.info(f"New session cart_id created: {session_cart_id}")
            
            cart_qs = Cart.objects.filter(cart_id=session_cart_id, product=product, is_ordered=False)
            if cart_qs.exists():
                cart_item = cart_qs.first()
                cart_item.quantity += quantity  # Update the quantity
            else:
                cart_item = Cart.objects.create(cart_id=session_cart_id, product=product, is_ordered=False, quantity=quantity)
            cart_item.save()
            messages.success(request, f"{product.title} is added to cart")

            # Create or update the order
            order, created = Order.objects.get_or_create(
                cart_id=session_cart_id,
                is_ordered=False,
                defaults={
                    'reference': f'order-{secrets.token_hex(8)}',
                    'date': timezone.now()
                }
            )

            if not order.product.filter(id=cart_item.id).exists():
                order.product.add(cart_item)
            order.save()

            storage = get_messages(request)
            response_messages = [{'message': message.message, 'tags': message.tags} for message in storage]

            cart_count = Cart.objects.filter(cart_id=session_cart_id, is_ordered=False).count()

            return JsonResponse({'success': True, 'cart_count': cart_count, 'messages': response_messages})
    return JsonResponse({'message': 'error processing your request'}, status=400)



def delete_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    next_url = request.GET.get('next')

    if request.user.is_authenticated:
        cart = Cart.objects.filter(product=product, user=request.user, is_ordered=False)
        order = Order.objects.filter(user=request.user, is_ordered=False).first()
        
        if order and order.product.filter(product=product).exists():
            cart.delete()
            messages.success(request, 'Deleted from cart')
        else:
            messages.error(request, 'You have already removed this item from the cart or no active order exists')
        
    else:
        session_cart_id = request.session.get('cart_id')
        if session_cart_id:
            cart = Cart.objects.filter(product=product, cart_id=session_cart_id, is_ordered=False)
            if cart.exists():
                cart.delete()
                messages.success(request, 'Deleted from cart')
            else:
                messages.error(request, 'Item not found in cart')
        else:
            messages.error(request, 'No active cart found in session')

    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect("store:index")




@login_required
def verify_address(request):
    # Fetch user's addresses
    user_addresses = CustomersAddress.objects.filter(user=request.user)
    
    # Fetch current order details
    orders = Order.objects.filter(user=request.user, is_ordered=False)
    
    total_order_cost = 0
    total_delivery_cost = 0
    total_cost_with_delivery = 0
    order = None
    order_items = []
    coupon = None

    if orders.exists():
        order = orders.first()
        total_order_cost = order.get_total()  # Assuming get_total() method calculates total cost
        total_delivery_cost = order.get_delivery_cost()  # Assuming get_delivery_cost() method calculates delivery cost
        total_cost_with_delivery = total_order_cost + total_delivery_cost
        order_items = order.product.all()  # Access the related products directly from the order
        if order.coupon:
            coupon = order.coupon

    context = {
        'addresses': user_addresses,
        'order': order,
        'total_order_cost': total_order_cost,
        'total_delivery_cost': total_delivery_cost,
        'total_cost_with_delivery': total_cost_with_delivery,
        'order_items': order_items,
        'coupon': [coupon] if coupon else None,
    }
    
    return render(request, 'store/check-user-address.html', context)

# checkout view
@login_required
class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = AddressForm(self.request.POST or None)
        coupon = Coupon.objects.filter(active=True)

        order = Order.objects.filter(user=self.request.user, is_ordered=False).first()
        cart = Cart.objects.filter(user=self.request.user, is_ordered=False)
        address = CustomersAddress.objects.filter(user=self.request.user)
        
        context = {
            'coupon': coupon,
            'order': {
                'form': form,
                'order': order,
                'cart': cart,
                'coupon': CouponForm()
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
                # payment_option = form.cleaned_data.get('payment_option')
                billing_address = CustomersAddress.objects.create(
                    user=self.request.user,
                    order=order,
                    street_address=street_address,
                    apartment=apartment,
                    town=town,
                    state=state,
                    country=country,
                    zip_code=zip_code,
                )
                
                order.shipping_address = billing_address
                order.save()
                return redirect('store:initiate_payment')
            print(order)
            messages.warning(self.request, 'Order failed')
            return redirect('store:cart')
                  
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have an active order')
            return redirect('store:categories')

# next_url = request.GET.get('next')  # Define next_url early in the code
 

def Update_addressView(request,pk):
    next_url = request.GET.get('next')  # Define next_url early in the code
    
    address = CustomersAddress.objects.get(user=request.user,pk=pk)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your address has been updated.')
            # if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            return redirect('store:verify-address')
            # messages.error(request, 'error updating your address')
            # return redirect('store:index')
    else:
        form = AddressForm(instance=address)
    
    context = {
        'form': form,
        'address': address
    }
    return render(request, 'store/update_address.html', context)

def initiate_payment(request):
    order = Order.objects.get(is_ordered=False, user=request.user)
    cart = Cart.objects.filter(user=request.user, is_ordered=False)

    if request.method == "POST":
        amount = request.POST['amount']
        email = request.POST['email']
        pk = settings.PAYSTACK_PUBLIC_KEY

        # Convert amount to float instead of int
        payment = Payment.objects.create(amount=float(amount), email=email, order=order, user=request.user)
        payment.save()

        context = {
            'payment': payment,
            'field_values': request.POST,
            'paystack_pub_key': pk,
            'amount_value': payment.amount_value(),
            'order': order         
        }
        
        return render(request, 'store/make-payment.html', context)

    return render(request, 'store/payment.html', {'order': order, 'cart': cart})


def verify_payment(request, ref):
    try:
        order = Order.objects.get(is_ordered=False, user=request.user)
        payment = Payment.objects.get(ref=ref)

        paystack_secret_key = settings.PAYSTACK_SECRET_KEY
        verify_url = f'https://api.paystack.co/transaction/verify/{ref}'
        headers = {
            'Authorization': f'Bearer {paystack_secret_key}',
            'Content-Type': 'application/json',
        }

        response = requests.get(verify_url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            paystack_amount = data['data']['amount'] / 100  # Convert kobo to naira
            expected_amount = order.get_total_with_delivery()

            if paystack_amount == expected_amount and data['data']['status'] == 'success':
                payment.verified = True
                payment.save()

                # Mark order products as ordered
                order_products = order.product.all()
                order_products.update(is_ordered=True)

                # Update order status and create invoice
                order.is_ordered = True
                order.payment = payment
                order.reference = create_ref_code()  # Assuming you have a function to create a reference code
                order.save()

                # Create invoice
                invoice = Invoice.objects.create(
                    invoice_number=generate_random_number(),  # Define/create your own function for generating invoice numbers
                    order=order,
                    payment=payment,
                    issued_at=timezone.now()
                    # Add more fields as needed
                )
                invoice.save()
                # Optionally, you can save additional invoice details here
                
                return render(request,'store/success.html', {'invoice': invoice, 'order': order, 'payment': payment})
            else:
                return render(request, 'store/payment_not_successful.html')

        else:
            print(f"Failed to verify payment. Status code: {response.status_code}, Paystack response: {response.text}")
            return JsonResponse({'status': 'error', 'message': 'Failed to verify payment.'})

    except Order.DoesNotExist:
        print("Order does not exist for the user.")
        return JsonResponse({'status': 'error', 'message': 'Order does not exist for the user.'})
    except Payment.DoesNotExist:
        print("Payment does not exist for the reference.")
        return JsonResponse({'status': 'error', 'message': 'Payment does not exist for the reference.'})
    except requests.exceptions.RequestException as e:
        print(f"Error verifying payment: {str(e)}")
        return JsonResponse({'status': 'error', 'message': f"Error verifying payment: {str(e)}"})



def success_page(request):
    return render(request, 'store/success.html')                      

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
    
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
        is_in_cart = Cart.objects.filter(product=product, is_ordered=False, user=request.user).exists()
        user_rating = CustomerRating.objects.filter(user=request.user, product=product).first()
    else:
        session_key = get_session_key(request)
        is_in_cart = Cart.objects.filter(product=product, is_ordered=False, session_key=session_key).exists()
        in_wishlist = Wishlist.objects.filter(session_key=session_key, product=product).exists()
        user_rating = None
    
    ratings = product.ratings.all()
    average_rating = product.average_rating()
    all_user_rating = product.ratings.filter(user=request.user) if request.user.is_authenticated else None
    next_product = product.get_next_product()
    related_products = product.get_related_products()
    
    if request.method == 'POST' and request.user.is_authenticated:
        rating_form = CustomerRatingForm(request.POST, instance=user_rating)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.user = request.user
            rating.product = product
            rating.save()
            return redirect('store:product-detail', slug=product.slug)
    else:
        rating_form = CustomerRatingForm(instance=user_rating) if request.user.is_authenticated else None

    context = {
        'product': product,
        'ratings': ratings,
        'average_rating': average_rating,
        'count': product.ratings.count(),
        'rating_form': rating_form,
        'now': timezone.now(),
        'all_user_rating': all_user_rating,
        'is_in_cart': is_in_cart,
        'next_product': next_product,
        'csrf_token': request.META.get('CSRF_COOKIE'),
        'related_products': related_products,
        'in_wishlist': in_wishlist,
    }
    
    return render(request, 'store/product_detail.html', context)


# this function enables users to delete a product from the cart
class DeleteCartItem(View):
    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            slug = request.POST.get('slug') # Ensure to convert the slug to an integer before using it
            product = get_object_or_404(Product, slug=slug) # Ensure to get the product using the primary key
            
            if request.user.is_authenticated: # Check if the user is authenticated
                cart_item = get_object_or_404(Cart, product=product, is_ordered=False, user=request.user) # Ensure to get the cart item using the product and user
                cart_item.delete() # Delete the cart item
            else:
                session_cart = request.session.get('cart', {}) # Get the cart from the session
                if str(slug) in session_cart: # Check if the product is in the cart
                    del session_cart[str(slug)] # Delete the product from the cart
                    request.session['cart'] = session_cart # Update the session cart

            return JsonResponse({ 
                'product': product.title,
                'slug': slug,
                'button_text': 'Add to Cart',
                'csrf_token': request.META.get('CSRF_COOKIE'),
            })
        
        return JsonResponse({'message': 'error'}, status=400)


class UpdateCartQuantity(View):
    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            id = int(self.request.POST.get('id'))
            quantity = request.POST.get('quantity')
            quantity1 = request.POST.get('quantity1')
            
            # Validate the quantity
            try:
                quantity = int(quantity) or int(quantity1)
            except (ValueError, TypeError):
                return JsonResponse({'message': 'Invalid quantity'}, status=400)
            
            size = request.POST.get('size')
            
            product = get_object_or_404(Product, pk=id)
            
            if request.user.is_authenticated:
                cart = get_object_or_404(Cart, product=product, is_ordered=False, user=request.user)
                
                cart.quantity = quantity
                cart.size = size if size else None  # Handle the case where size is not provided
                
                cart.save()
            else:
                session_cart = request.session.get('cart', {})
                
                if str(id) in session_cart:
                    session_cart[str(id)]['quantity'] = quantity
                    session_cart[str(id)]['size'] = size if size else None  # Handle the case where size is not provided
                else:
                    session_cart[str(id)] = {
                        'quantity': quantity,
                        'size': size if size else None
                    }
                
                request.session['cart'] = session_cart

            if product.discount_price:
                total_price = product.discount_price * quantity
            else:
                total_price = product.price * quantity

            messages = [{'message': 'Cart updated successfully', 'tags': 'success'}]

            return JsonResponse({
                'product': product.title,
                'id': id,
                'qty': quantity,
                'size': size,  # Ensure to return size even if it's None
                'total_price': total_price,
                'messages': messages
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



def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    session_key = get_session_key(request) if not request.user.is_authenticated else None

    if request.user.is_authenticated:
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    else:
        wishlist_item, created = Wishlist.objects.get_or_create(session_key=session_key, product=product)

    if created:
        message = "Added to wishlist"
        in_wishlist = True
    else:
        wishlist_item.delete()
        message = "Removed from wishlist"
        in_wishlist = False

    return JsonResponse({'message': message, 'in_wishlist': in_wishlist})



def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        Wishlist.objects.filter(user=request.user, product=product).delete()
    else:
        session_key = get_session_key(request)
        Wishlist.objects.filter(session_key=session_key, product=product).delete()

    return JsonResponse({'message': "Removed from wishlist"})



def wishlist(request):
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    else:
        session_key = get_session_key(request)
        wishlist_items = Wishlist.objects.filter(session_key=session_key).select_related('product')
    
    # Fetch stock information
    for item in wishlist_items:
        item.stock_quantity = Stock.objects.get(product=item.product).quantity
    
    context = {
        'wishlist': wishlist_items
    }
    
    return render(request, 'store/wishlist.html', context)



def wishlist_count(request):
    if request.user.is_authenticated:
        count = Wishlist.objects.filter(user=request.user).count()
    else:
        session_key = get_session_key(request)
        count = Wishlist.objects.filter(session_key=session_key).count()

    return JsonResponse({'count': count})





