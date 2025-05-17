from django.urls import path
from .views import (
    search_device,
    DeviceViewSet,
    search_device_socket,
    client_device,
    KeyDevice, add_psychrometer_to_relay6, UpdatePsychrometerAPIView, PsychrometerImageView,
)

urlpatterns = [
    path("", DeviceViewSet.as_view(), name="device-list"),
    path("raw/", KeyDevice.as_view(), name="list"),
    path("psy-image/", PsychrometerImageView.as_view(), name="psy-images"),
    path("<str:device_id>/", search_device, name="search"),
    path("socket/<str:device_id>/", search_device_socket, name="docket"),
    path("client/<str:device_id>/", client_device, name="client"),
    path('relay6/<uuid:relay6_id>/add_psychrometer/', add_psychrometer_to_relay6,
         name='add_psychrometer_to_relay6_api'),
    path("relay6/<uuid:relay6_id>/port/<int:port>/psychrometer/", UpdatePsychrometerAPIView.as_view(),
         name="update-psychrometer"),
]
