
from django.urls import path

from catalog import views
from catalog.views import ProductListView, ProductDetailView, ProductCreateView, AddContact

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('contacts/', AddContact.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='about_product'),
    path('place_a_product/', ProductCreateView.as_view(), name='place_a_product')
]
