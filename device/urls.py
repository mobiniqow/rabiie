from django.urls import path
from .views import search_device, DeviceViewSet, search_device_socket, client_device, KeyDevice

urlpatterns = [
    path('', DeviceViewSet.as_view(), name='device-list'),
    path('raw/', KeyDevice.as_view(), name='list'),
    path('<str:device_id>/', search_device, name='search'),
    path('socket/<str:device_id>/', search_device_socket, name='docket'),
    path('client/<str:device_id>/', client_device, name='client'),
]
