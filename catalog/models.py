from django.db import models


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(
        max_length=150,
        verbose_name="Наименование продукта",
        help_text="Ведите наименование продукта",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание продукта",
        help_text="Ведите описание продукта",
    )
    image = models.ImageField(
        upload_to="catalog/image",
        blank=True,
        null=True,
        verbose_name="Фото продукта",
        help_text="Загрузите фото продукта",
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Категория продукта",
        help_text="Ведите категорию продукта",
        related_name="products",
    )
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Строковое отображение объекта
        return f"{self.product_name} {self.category} {self.price}"

    class Meta:
        verbose_name = "продукт"  # Настройка для наименования одного объекта
        verbose_name_plural = "продукты"  # Настройка для наименования набора объектов
        ordering = ["product_name", "price", "category"]


class Category(models.Model):
    category_name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    def __str__(self):
        # Строковое отображение объекта
        return self.category_name

    class Meta:
        verbose_name = "категория"  # Настройка для наименования одного объекта
        verbose_name_plural = "категории"  # Настройка для наименования набора объектов
        ordering = ["category_name"]
