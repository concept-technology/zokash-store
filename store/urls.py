from . import views
from django.urls import path
app ='store'

urlpatterns = [
    path('', views.store, name='store')
]
