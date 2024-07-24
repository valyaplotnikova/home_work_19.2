from django.db import models, connection


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
        verbose_name="Фото",
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
    price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Строковое отображение объекта
        return f"{self.product_name} {self.category} {self.price}"

    @classmethod
    def truncate_table_restart_id(cls):
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE {cls._meta.db_table} RESTART IDENTITY CASCADE')

    class Meta:
        verbose_name = "продукт"  # Настройка для наименования одного объекта
        verbose_name_plural = "продукты"  # Настройка для наименования набора объектов
        ordering = ["product_name", "price", "category"]


class Category(models.Model):
    category_name = models.CharField(
        max_length=150,
        verbose_name="Категория продукта",
        help_text="Ведите категорию продукта",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание категории",
        help_text="Ведите описание категории",
    )

    def __str__(self):
        # Строковое отображение объекта
        return self.category_name

    @classmethod
    def truncate_table_restart_id(cls):
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE {cls._meta.db_table} RESTART IDENTITY CASCADE')

    class Meta:
        verbose_name = "категория"  # Настройка для наименования одного объекта
        verbose_name_plural = "категории"  # Настройка для наименования набора объектов
        ordering = ["category_name"]


class Contacts(models.Model):
    user_name = models.CharField(
        max_length=150,
        verbose_name="Имя пользователя",
        help_text="Ведите имя пользователя",
    )
    phone = models.CharField(
        max_length=50,
        verbose_name="Номер телефона",
        help_text="Ведите номер телефона",
    )
    massage = models.TextField(
        blank=True,
        null=True,
        verbose_name="Сообщение",
        help_text="Ведите сообщение",
    )

    def __str__(self):
        # Строковое отображение объекта
        return f'{self.user_name} {self.phone}'

    class Meta:
        verbose_name = "контакты"  # Настройка для наименования одного объекта
        verbose_name_plural = "контакты"  # Настройка для наименования набора объектов
        ordering = ["user_name"]
