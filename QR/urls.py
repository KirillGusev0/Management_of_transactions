from django.urls import path
from . import views

app_name = "QR"

urlpatterns = [
    path("generate/", views.generate_qr, name="generate_qr"),
    path("product/<int:product_id>/", views.product_detail_by_id, name="product_detail_by_id"),
    path("<uuid:uuid>/", views.product_detail_by_uuid, name="product_detail_by_uuid"),
    path("add/", views.add_product, name="add_product"),
]