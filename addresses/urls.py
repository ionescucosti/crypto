from django.urls import path, include
from addresses.views import *


urlpatterns = [
    path('', home_view, name='home'),
    path('generate/<str:currency>/', generate_address, name='generate_address'),
    path('list/', get_list, name='list'),
    path('address/<int:address_id>/', get_address, name='get_addresses'),
]
