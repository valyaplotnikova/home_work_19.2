import json
from django.core.management import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        """Получаем данные о категориях из фикстуры в формате json"""
        with open('fixtures/category.json', 'r', encoding='utf-8') as file:
            categories = json.load(file)
            return categories

    @staticmethod
    def json_read_products():
        """Получаем данные о продуктах из фикстуры в формате json"""
        with open('fixtures/product.json', 'r', encoding='utf-8') as file:
            products = json.load(file)
            return products

    def handle(self, *args, **options):
        # Удаляем все продукты из базы данных
        Product.truncate_table_restart_id()
        # Удаляем все категории из базы данных
        Category.truncate_table_restart_id()

        # Создаем списки для хранения объектов категорий и продуктов
        product_for_create = []
        category_for_create = []

        # Обходим все значения категорий из фикстуры для получения информации
        # об одном объекте
        for category in Command.json_read_categories():
            category_for_create.append(
                Category(
                    category_name=category['fields']['category_name'],
                    description=category['fields']['description'],

                )
            )

        # Создаем объекты категорий в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        # Обходим все значения продуктов из фикстуры для получения информации
        # об одном объекте
        for product in Command.json_read_products():

            product_for_create.append(
                Product(
                    product_name=product['fields']['product_name'],
                    description=product['fields']['description'],
                    price=product['fields']['price'],
                    image=product['fields']['image'],
                    created_at=product['fields']['created_at'],
                    updated_at=product['fields']['updated_at'],
                    category=Category.objects.get(pk=product['fields']['category']),
                )
            )

        # Создаем объекты продуктов в базе с помощью метода bulk_create()
        Product.objects.bulk_create(product_for_create)
