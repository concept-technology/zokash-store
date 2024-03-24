from . import views
from django.urls import path
# app_name ='store'

urlpatterns = [
    path('', views.index, name='index'),
    # path('catalogue/', views.index, name='catalogue'),
    path('catalogue/<int:pk>', views.catalogue_item, name='catalogue_item')
]
