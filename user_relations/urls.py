from django.urls import path
from .views import UserChildManipulation

urlpatterns = [
    path(
        "user-childs/",
        UserChildManipulation.as_view(),
        name="add-remove-change-user-child",
    ),
    path(
        "user-childs/<int:user_child_id>/",
        UserChildManipulation.as_view(),
        name="change-user-child-state",
    ),
]
