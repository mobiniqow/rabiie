from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RoomView, RoomPictureList, RoomDeviceListAPIView

router = DefaultRouter()
router.register("", RoomView, basename="rooms")

urlpatterns = [
    path("images/", RoomPictureList.as_view(), name="rooms"),
    path("devices/<int:room_id>/", RoomDeviceListAPIView.as_view(), name="devices"),
    path("", include(router.urls), name="rooms"),
]
