from django.urls import path, include
from .views import (
    VerifyUser,
    LoginUser,
    UserProfile,
    get_user_by_national_id,
    get_access,
)
from rest_framework import routers
from .views import UserViewSet, terms_and_conditions

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("login", LoginUser.as_view()),
    path("terms", terms_and_conditions),
    # access
    path("verify", VerifyUser.as_view()),
    path("profile", UserProfile.as_view()),
    path("", include(router.urls)),
]

# todo vase amar moameat mitonam begam onaie ke to list alan nabodan ro hazv kon va create or update konam
