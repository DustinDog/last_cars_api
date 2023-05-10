from django.urls import path

from core.views import CreateUserView, LoginView, Healthcheck

urlpatterns = [
    path("healthcheck/", Healthcheck.as_view()),
    path("user/create/", CreateUserView.as_view(), name="create_user"),
    path("user/login/", LoginView.as_view(), name="login"),
]
