from django.urls import path
from rest_framework import routers


from core.views import (
    CreateUserView,
    LoginView,
    FavouritesViewSet,
    ActivateUserView,
    UserProfileView,
    PasswordUpdateView,
)


router = routers.SimpleRouter()
router.register(r"favourites", FavouritesViewSet)


urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create_user"),
    path("login/", LoginView.as_view(), name="login"),
    path("activate/", ActivateUserView.as_view(), name="activate"),
    path("my-profile/", UserProfileView.as_view(), name="myprofile"),
    path("update-password/", PasswordUpdateView.as_view(), name="update_password"),
]
urlpatterns.extend(router.urls)
