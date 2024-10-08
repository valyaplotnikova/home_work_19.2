from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError, PermissionDenied
from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse

from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView, DeleteView


from catalog.forms import AddContactForm, AddProductForm, VersionForm, VersionFormset, ProductModeratorForm
from catalog.models import Product, Version, Category
from catalog.services import get_categories_from_cache, get_product_from_cache


class CategoryListView(ListView):
    model = Category

    def get_queryset(self):
        return get_categories_from_cache()


class ProductListView(ListView):
    model = Product
    paginate_by = 3

    def get_queryset(self):
        return get_product_from_cache()

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        products = self.get_queryset()
        for product in products:
            active_versions = Version.objects.filter(product_id=product.pk, is_version_active=True)
            if active_versions:
                product.active_name = active_versions.last().version_name
                product.active_number = active_versions.last().version_number
            else:
                product.active_name = 'Отсутствует'
                product.active_number = 'Отсутствует'

        context_data['object_list'] = products

        return context_data


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, form=VersionForm, formset=VersionFormset, extra=1)
        if self.request.method == 'POST':
            formset = ProductFormset(self.request.POST, instance=self.object)
        else:
            formset = ProductFormset(instance=self.object)
        context_data['formset'] = formset
        return context_data


class ProductCreateView(CreateView, LoginRequiredMixin):
    model = Product
    form_class = AddProductForm
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product


    def get_success_url(self):
        return reverse('catalog:about_product', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, VersionForm, formset=VersionFormset, extra=1)

        if self.request.method == 'POST':
            context_data['formset'] = ProductFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = ProductFormset(instance=self.object)
        return context_data

    def get_form_class(self):
        user = self.request.user
        if user.is_superuser:
            return AddProductForm
        elif user == self.object.owner:
            return AddProductForm
        # elif user.groups.filter(name='moderator').exists():
        elif (user.has_perm('catalog.can_edit_description') and user.has_perm('catalog.can_edit_category')
              and user.has_perm('catalog.can_edit_is_published')):
            return ProductModeratorForm
        else:
            raise PermissionDenied

    def form_valid(self, form):
        """Метод для сохранения формы при редактировании"""
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        else:
            form.add_error(None, ValidationError("Only one version can be active at a time."))
            return self.form_invalid(form)
        return super().form_valid(form)


class ProductDeleteView(DeleteView, LoginRequiredMixin):
    model = Product
    success_url = reverse_lazy('product_list')


class AddContact(FormView):
    form_class = AddContactForm
    template_name = 'catalog/contacts.html'
    success_url = reverse_lazy('product_list')
