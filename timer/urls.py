from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DeviceTimerView


router = DefaultRouter()
router.register("", DeviceTimerView, basename="rooms")

urlpatterns = [
    path(
        "", include(router.urls)
    )
]
