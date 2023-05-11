from rest_framework import routers
from django.urls import include, path

from cars.views import (
    BrandListAPIView,
    ModelListAPIView,
    CarViewSet,
)

router = routers.SimpleRouter()
router.register(r"", CarViewSet)

urlpatterns = [
    path("brands/", BrandListAPIView.as_view(), name="brand_list"),
    path("models/", ModelListAPIView.as_view(), name="model_list"),
    path("", include(router.urls), name="cars"),
]
