from django.urls import path
from .views import UserDeviceView, UserRelayDeviceView

urlpatterns = [
    path('user-devices/', UserDeviceView.as_view(), name='user-devices'),
    path('user-devices/<int:user_device_id>/', UserDeviceView.as_view(), name='user-device-detail'),
    path('user-relay-devices/', UserRelayDeviceView.as_view(), name='user-relay-devices'),
    path('user-relay-devices/<int:user_relay_device_id>/', UserRelayDeviceView.as_view(), name='user-relay-device-detail'),
    path('user-relay-devices/<int:user_relay_device_id>/user-devices/', UserRelayDeviceView.as_view(), name='user-device-on-relay'),
    path('user-relay-devices/<int:user_relay_device_id>/user-devices/<int:user_device_id>/', UserRelayDeviceView.as_view(), name='add-remove-user-device'),
]