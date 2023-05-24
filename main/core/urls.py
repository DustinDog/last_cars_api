from django.urls import path
from rest_framework import routers


from core.views import (
    CreateUserView,
    LoginView,
    MyListingsViewSet,
    ActivateUserView,
)


router = routers.SimpleRouter()
router.register(r"my-listings", MyListingsViewSet)


urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create_user"),
    path("login/", LoginView.as_view(), name="login"),
    path("activate/", ActivateUserView.as_view(), name="activate"),
]
urlpatterns.extend(router.urls)
