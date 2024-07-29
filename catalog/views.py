from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView, FormView


from catalog.forms import AddContactForm
from catalog.models import Product, Contacts


class ProductListView(ListView):
    model = Product
    paginate_by = 3


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    fields = ('product_name', 'description', 'image', 'category', 'price')
    success_url = reverse_lazy('product_list')


class AddContact(FormView):
    form_class = AddContactForm
    template_name = 'catalog/contacts.html'
    success_url = reverse_lazy('product_list')
