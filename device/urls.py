from django.urls import path
from .views import search_device, DeviceViewSet

urlpatterns = [
    path('<str:product_id>/', search_device, name='search'),
    path('', DeviceViewSet.as_view(), name='search'),
]
