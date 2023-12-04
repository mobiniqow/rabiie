from django.urls import path
from .views import RoomView, RoomDeviceView

urlpatterns = [
    path('rooms/', RoomView.as_view(), name='rooms'),
    path('room-devices/', RoomDeviceView.as_view(), name='room-devices'),
]
