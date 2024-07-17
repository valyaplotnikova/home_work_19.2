import json

from django.shortcuts import render

from catalog.models import Product


def home(request):
    print(Product.objects.all().order_by('-created_at')[:5])
    return render(request, 'catalog/home.html')


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
