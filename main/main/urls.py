from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from django.contrib import admin
from core.views import CreateUserView, LoginView
from cars.views import (
    BrandListAPIView,
    ModelListAPIView,
    CarListAllAPIView,
    CarListCreateAPIView,
)


urlpatterns = [
    path("api/admin/", admin.site.urls),
    path("api/user/create/", CreateUserView.as_view(), name="create_user"),
    path("api/user/login/", LoginView.as_view(), name="login"),
    path("api/brands/", BrandListAPIView.as_view(), name="brand_list"),
    path("api/models/", ModelListAPIView.as_view(), name="model_list"),
    path("api/cars/all/", CarListAllAPIView.as_view(), name="car_list_all"),
    path("api/cars/", CarListCreateAPIView.as_view(), name="list_create"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("__debug__/", include("debug_toolbar.urls")),
]
