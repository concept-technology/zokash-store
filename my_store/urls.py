from django.urls import path
from . import views


app_name ='store'

urlpatterns = [
     path('submit_rating/', views.product_detail, name='submit_rating'),
     
     
    path('category/', views.ProductCategories_view, name='categories-list'),
    
    path('category/<slug>/', views.product_list_by_category, name='product_list_by_category'),
    
#     path('categories/<str:title>', views.category_filter, name='categories-filter'),

    path('', views.HomeView.as_view(),name='index'),
      
    path('signup/',views.register, name='signup'),
    
    path('login', views.login, name='login'),
    
    path('catalogue/<slug>', views.ProductDetailView.as_view(),name='store_item'),

     path('add-to-cart/<slug>',views.add_to_cart, name='add-to-cart'),
     
     path('delete-cart/<slug>',views.delete_cart, name='delete_cart'),
     
     path('cart/check-out',views.CheckoutView.as_view(), name='check-out'),
     
     path('cart/', views.CartView.as_view(), name='cart'),
     
     path('cart/<slug>', views.CartView.as_view(), name='cart_item'),
     
     path('account/dash-board',views.dash_board, name='dash-board' ),
     
     path('reduce-item-from-cart/<slug>', views.reduce_cart_quantity, name='remove_cart'),
     
     path('increase-cart-quantity/<slug>', views.increase_cart_quantity, name='increase_cart'),
     
     path('order/payment/', views.initiate_payment, name='initiate_payment'),
     
     path('verify-payment/<str:ref>/', views.verify_payment, name='verify_payment'),
     
     path('refund-request', views.RequestRefund.as_view(), name='refund-request'),
     
     path('verify-address', views.verify_address, name='verify-address'),
     
     path('address/edit/<int:pk>', views.Update_addressView, name='update-address'),
     
     
     path('apply-coupon/', views.apply_coupon, name='apply-coupon'),
     
     path('select-address/', views.select_shipping_method, name='select_address'),


     path('search/', views.search_view, name='search'),
     
     path('product/<slug>', views.product_detail, name='product-detail'),
     
     path('update-cart/', views.UpdateCartQuantity.as_view(), name='update_cart_quantity'),
     
 
]


