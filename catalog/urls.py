
from django.urls import path

from catalog import views


urlpatterns = [
    path('', views.home),
    path('contacts/', views.contacts, name='contacts'),
    path('product/<int:pk>/', views.about_product, name='about_product')
]
