from django.urls import path
from .views import search_device, DeviceViewSet, search_device_socket

urlpatterns = [
    path('<str:product_id>/', search_device, name='search'),
    path('socket/<str:product_id>/', search_device_socket, name='search'),
    path('', DeviceViewSet.as_view(), name='device-list'),
]
