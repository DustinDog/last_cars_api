from django.urls import path
from rest_framework import routers


from core.views import CreateUserView, LoginView, MyListingsViewSet


router = routers.SimpleRouter()
router.register(r"my-listings", MyListingsViewSet)


urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create_user"),
    path("login/", LoginView.as_view(), name="login"),
]
urlpatterns.extend(router.urls)
