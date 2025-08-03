from django.urls import path
from . import views

app_name = 'contacts_import_export'

urlpatterns = [
    path('upload/', views.upload_contacts, name='upload_contacts'),
    path('export/', views.export_contacts, name='export_contacts'),
]