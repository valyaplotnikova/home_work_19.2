import json

from django.shortcuts import render, get_object_or_404

from catalog.models import Product


def home(request):
    product_list = Product.objects.all()
    context = {
        "object_list": product_list
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

    return render(request, 'catalog/contacts.html')


def about_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        "product": product
    }
    return render(request, 'catalog/about_product.html', context)

