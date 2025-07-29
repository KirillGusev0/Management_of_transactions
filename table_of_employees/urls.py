from django.urls import path
from table_of_employees import views

app_name = "table_of_employees"

urlpatterns = [
    path('', views.employee_table, name='employee_table'),
]