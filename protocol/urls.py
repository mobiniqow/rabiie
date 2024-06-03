from django.urls import path
from .views import EventSocket

urlpatterns = [
    path("send-message/", EventSocket.as_view(), name="send-message"),
]
