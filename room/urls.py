from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RoomView, RoomDeviceView

router = DefaultRouter()
router.register('', RoomView, basename='rooms')

urlpatterns = [
    path('', include(router.urls), name='rooms'),
    path('devices/<int:room_id>/', RoomDeviceView.as_view(), name='devices'),
]
