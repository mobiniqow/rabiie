from django.urls import path
from .views import search_device, DeviceViewSet, search_device_socket, client_device

urlpatterns = [
    path('<str:product_id>/', search_device, name='search'),
    path('socket/<str:product_id>/', search_device_socket, name='docket'),
    path('client/<str:client_id>/', client_device, name='client'),
    path('', DeviceViewSet.as_view(), name='device-list'),
]
