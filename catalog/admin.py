from django.contrib import admin
from catalog.models import Product, Category, Contacts, Version


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    ist_display = ('ID', 'product_name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('product_name', 'description')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ist_display = ('ID', 'category_name')
    search_fields = ('category_name', 'description')


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'phone', 'massage')
    search_fields = ('user_name', 'phone')


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('product', 'version_number', 'version_name', 'is_version_active')
    search_fields = ('product', 'version_number')