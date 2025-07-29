from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from QR.models import ProductLink
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
import qrcode
from io import BytesIO
from django.http import HttpResponse
import os
from django.conf import settings
from integration_utils.bitrix24.bitrix_token import BaseBitrixToken
from .forms import ProductForm
from .models import Product, ProductLink

@main_auth()
def generate_qr(request):
    # Проверка и создание директории media/qrcodes
    qr_folder = os.path.join(settings.MEDIA_ROOT, 'qrcodes')
    if not os.path.exists(qr_folder):
        os.makedirs(qr_folder)

    """
    Страница с формой для ввода product_id и генерации QR
    """
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        link = ProductLink.objects.create(product_id=product_id)
        # URL, который будет в QR
        full_url = request.build_absolute_uri(
            reverse("QR:product_detail_by_uuid", args=[str(link.uuid)])
        )

        # Генерация QR кода
        qr = qrcode.make(full_url)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        buffer.seek(0)

        return HttpResponse(buffer.getvalue(), content_type="image/png")

    return render(request, "QR/generate_qr.html")
@main_auth()
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect('QR:product_detail_by_id', product_id=product.id)
    else:
        form = ProductForm()
    return render(request, 'QR/add_product.html', {'form': form})



def product_detail_by_uuid(request, uuid):
    """
    Публичная страница с данными о товаре (по UUID)
    """
    link = get_object_or_404(ProductLink, uuid=uuid)

    try:
        product = Product.objects.get(id=link.product_id)
    except Product.DoesNotExist:
        product = None

    if not product:
        return render(
            request,
            "QR/product_detail.html",
            {"error": "Товар не найден или был удалён"}
        )

    return render(
        request,
        "QR/product_detail.html",
        {"product": product}
    )


@main_auth()
def product_detail_by_id(request, product_id):
    """
    Страница с данными о товаре (по ID в БД)
    """
    product = get_object_or_404(Product, id=product_id)
    return render(request, "QR/product_detail.html", {"product": product})