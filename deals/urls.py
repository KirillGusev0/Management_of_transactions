from django.urls import path
from deals.views.active_deals import active_deals
from deals.views.add_deal import add_deal

urlpatterns = [
    path('add_deal/', add_deal, name="add_deal"),
    path('active_deals/', active_deals, name="active_deals"),
]