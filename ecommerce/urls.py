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
     
     path('delete-from-cart/<slug>',views.delete_cart, name='delete_cart_on_cart_page'),
     
     path('cart/', views.CartView.as_view(), name='cart'),
     
     path('account/dash-board',views.dash_board, name='dash-board' )
     
]

