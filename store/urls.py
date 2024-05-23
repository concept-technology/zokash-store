from django.urls import path
from . import views
app_name ='store'

urlpatterns = [
    path('categories', views.ProductCategoriesView.as_view(), name='categories'),

    path('', views.HomeView.as_view(),
         name='index'),
      
    path('signup/',views.register,         
         name='signup'),
    
    path('login', views.login, name='login'),
    
    path('catalogue/<slug>', 
         views.ProductDetailView.as_view(),
         name='store_item'),

     path('add-to-cart/<slug>',views.add_to_cart, name='add-to-cart'),
     
     path('delete-cart/<slug>',views.delete_cart, name='delete_cart'),
     
     path('cart/check-out',views.CheckoutView.as_view(), name='check-out'),
     
     path('cart/', views.CartView.as_view(), name='cart'),
     
     path('cart/<slug>', views.CartView.as_view(), name='cart_item'),
     
     path('account/dash-board',views.dash_board, name='dash-board' ),
     
     path('reduce-item-from-cart/<slug>', views.reduce_cart_quantity, name='remove_cart'),
     
     path('increase-cart-quantity/<slug>', views.increase_cart_quantity, name='increase_cart'),
     
     path('checkout/payment', views.PaymentView.as_view(), name='payment'),
     
     
     path('payment/', views.initiate_payment, name='initiate_payment'),
     path('verify-payment/<str:ref>/', views.verify_payment, name='verify_payment'),
     
     path('not_varified/', views.not_varified, name='not_varified')
     
]

