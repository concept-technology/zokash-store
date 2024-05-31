from django.urls import include, path
from .import views
app_name = 'api'
urlpatterns = [
    path('product/', views.ProductView.as_view(), name='product_view'),
    path('product/<int:pk>', views.ProductSingleItemView.as_view(), name='product_single_view'),
    path('category/', views.ProductCategoryView.as_view(), name='product_category_view'),
    path('category/<int:pk>', views.ProductCategorySingleItemView.as_view(), name='product_category_single_view'),
    # path('catalogue/', views.Catalogue.as_view(), name='catalogue'),
    path('home', views.index, name='home')
]

