import json

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from catalog.forms import AddProductForm
from catalog.models import Product, Contacts


def home(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "object_list": product_list,
        'page_obj': page_obj
    }
    return render(request, 'catalog/home.html', context)


def contacts(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        data = [{'name': name, 'phone': phone, 'message': message}]

        print(f'{name}({phone}) - {message}')
        with open('fixtures/contacts.json', 'a', encoding='UTF-8') as file:
            json.dump(data, file, ensure_ascii=False)
            file.write('\n')

    contacts_list = Contacts.objects.all()
    context = {
            'contacts': contacts_list
        }
    return render(request, 'catalog/contacts.html', context)


def about_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        "product": product
    }
    return render(request, 'catalog/about_product.html', context)


def place_a_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = AddProductForm()

    context = {
        "form": form
    }
    return render(request, 'catalog/place_a_product.html', context)
