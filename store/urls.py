from . import views
from django.urls import path
app_name ='store'

urlpatterns = [
    path('', views.StoreView.as_view(), name='index'),
    path('sign-up/', views.StoreView.as_view(), name='sign-up'),
    # path('catalogue/', views.index, name='catalogue'),
    path('catalogue/<slug>', views.StoreItemView.as_view(), name='store_item'),
    # path('checkout/', views.checkout, name='checkout'),
    path('sign-upp/', views.sign_up, name='sign-up'),
    path('add-to-cart/<slug>', views.add_to_cart, name='add-to-cart'),
    path('delete_cart/<slug>', views.delete_cart, name='delete_cart')
]
