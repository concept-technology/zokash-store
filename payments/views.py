from django.shortcuts import render, redirect
from .models import Payment, UserWallet
from django.conf import settings
from store.models import Order,Cart


def initiate_payment(request):
    order = Order.objects.filter(is_ordered=False, user=request.user)
    cart =Cart.objects.filter(user=request.user, is_ordered=False)
    if request.method == "POST":
        amount = request.POST['amount']
        email = request.POST['email']

        pk = settings.PAYSTACK_PUBLIC_KEY

        payment = Payment.objects.create(amount=amount, email=email, user=request.user)
        payment.save()

        context = {
            'payment': payment,
            'field_values': request.POST,
            'paystack_pub_key': pk,
            'amount_value': payment.amount_value(),
            'order':order
            
        }
        return render(request, 'store/make-payment.html', context)

    return render(request, 'store/payment.html', {'order':order,'cart':cart})


def verify_payment(request, ref):
    payment = Payment.objects.get(ref=ref)
    verified = payment.verify_payment()
    if verified:
        order = Order.objects.get(is_ordered=False, user=request.user)
        
        # user_wallet = UserWallet.objects.get(user=request.user)
        # user_wallet.balance += payment.amount
        # user_wallet.save()
        order.is_ordered = True
        print(request.user.username, "successful")
        return render(request, "success.html")
    return render(request, "store/success.html")