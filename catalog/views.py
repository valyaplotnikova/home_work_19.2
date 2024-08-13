from django.forms import inlineformset_factory
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView, DeleteView

from catalog.forms import AddContactForm, AddProductForm, VersionForm
from catalog.models import Product, Contacts, Version


class ProductListView(ListView):
    model = Product
    paginate_by = 3


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            formset = ProductFormset(self.request.POST, instance=self.object)
        else:
            formset = ProductFormset(instance=self.object)
        context_data['formset'] = formset
        return context_data


class ProductCreateView(CreateView):
    model = Product
    form_class = AddProductForm
    success_url = reverse_lazy('product_list')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = AddProductForm
    success_url = reverse_lazy('product_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            formset = ProductFormset(self.request.POST, instance=self.object)
        else:
            formset = ProductFormset(instance=self.object)
        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        for form in formset:
            print(form.errors)
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')


class AddContact(FormView):
    form_class = AddContactForm
    template_name = 'catalog/contacts.html'
    success_url = reverse_lazy('product_list')
