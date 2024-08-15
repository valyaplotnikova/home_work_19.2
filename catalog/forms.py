from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Category, Product, Contacts, Version


class AddProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Жанр не выбран", label="Жанр книги")

    class Meta:
        model = Product
        fields = ['product_name', 'description', 'image', 'category', 'price']

        labels = {
            'price': 'Цена книги'
        }

    forbidden_words = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]

    def clean_product_name(self):
        cleaned_data = self.cleaned_data['product_name']
        for forbidden_word in self.forbidden_words:
            if forbidden_word in cleaned_data.lower():
                raise ValidationError(f'Наименование не должно содержать слово "{forbidden_word}"')
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        for forbidden_word in self.forbidden_words:
            if forbidden_word in cleaned_data.lower():
                raise ValidationError(f'Описание не должно содержать слово "{forbidden_word}"')
        return cleaned_data


class AddContactForm(forms.ModelForm):

    class Meta:
        model = Contacts
        fields = ['user_name', 'phone', 'massage']
        widgets = {
            'user_name': forms.TextInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'massage': forms.Textarea(attrs={'cols': 30, 'rows': 5}),
        }


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['product', 'version_number', 'version_name', 'is_version_active']


class VersionFormset(BaseInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
            if form.instance.is_version_active:
                count += 1
                if count > 1:
                    raise forms.ValidationError("Может быть только 1 активная версия")