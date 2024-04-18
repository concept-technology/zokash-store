from . import views
from django.urls import path

app_name ='store'

urlpatterns = [
    path('', views.StoreView.as_view(),
         name='index'),
    path('signup/',views.register,         
         name='signup'),
    
    path('login', views.login, name='login'),
    path('catalogue/<slug>', 
         views.StoreItemView.as_view(),
         name='store_item'),
    
    path('add-to-cart/<slug>', 
         views.add_to_cart, name='add-to-cart'),
    
    path('delete_cart/<slug>', 
         views.delete_cart, name='delete_cart'), 
    
    
   
]
