from django.contrib import admin
from .models import Product, ProductLink

@admin.register(ProductLink)
class ProductLinkAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'uuid', 'created_at')
    search_fields = ('product_id',)
    admin.site.register(Product)
    admin.site.register(ProductLink)