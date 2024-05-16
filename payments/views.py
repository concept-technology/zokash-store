from django.shortcuts import render, get_object_or_404
from .paystack import PayStack
from store.models import Order
from django.contrib import messages
from django.http import JsonResponse
from  store.models import Cart
from payments.models import Payments

# Create your views here.
    
    
def verify_payment(request, ref):
    
    cart = Cart(request)
    # payment = PaymentModel.objects.get(ref=ref)
    
    
    