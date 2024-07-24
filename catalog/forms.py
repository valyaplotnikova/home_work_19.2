from django import forms
from .models import Category, Product


class AddProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Жанр не выбран", label="Жанр книги")
    class Meta:
        model = Product
        fields = ['product_name', 'description', 'image', 'category', 'price']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }
        labels = {
            'price': 'Цена книги'
        }
