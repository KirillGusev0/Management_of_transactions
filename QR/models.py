from django.db import models
import uuid

class ProductLink(models.Model):
    """
    Уникальных ссылки на товар.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    product_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_id} ({self.uuid})"

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название товара")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Фото товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена", null=True, blank=True)

    def __str__(self):
        return self.name