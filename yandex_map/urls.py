from django.urls import path
from . import views

urlpatterns = [
    path("", views.company_map, name="company_map"),
]