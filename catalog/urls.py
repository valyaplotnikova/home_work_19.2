
from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, ProductCreateView, AddContact, ProductUpdateView, \
    ProductDeleteView, CategoryListView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('contacts/', AddContact.as_view(), name='contacts'),
    path('product/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='about_product'),
    path('place_a_product/', ProductCreateView.as_view(), name='place_a_product'),
    path('update_product/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('delete_product/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    path('category_list/', CategoryListView.as_view(), name='category_list'),
]
