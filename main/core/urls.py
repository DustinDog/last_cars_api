from core.views import (
    ActivateUserView,
    CreateUserView,
    EmailUpdateView,
    FavouritesViewSet,
    LoginView,
    PasswordUpdateView,
    UserProfileView,
)
from django.urls import path
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r"favourites", FavouritesViewSet)


urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create_user"),
    path("login/", LoginView.as_view(), name="login"),
    path("activate/", ActivateUserView.as_view(), name="activate"),
    path("my-profile/", UserProfileView.as_view(), name="myprofile"),
    path("update-password/", PasswordUpdateView.as_view(), name="update_password"),
    path("update-email/", EmailUpdateView.as_view(), name="update_email"),
]
urlpatterns.extend(router.urls)
