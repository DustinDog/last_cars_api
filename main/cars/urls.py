from cars.views import BrandListAPIView, CarViewSet, ModelListAPIView
from django.urls import include, path
from rest_framework import routers

router = routers.SimpleRouter()

router.register(r"cars", CarViewSet)


urlpatterns = [
    path("brands/", BrandListAPIView.as_view(), name="brand_list"),
    path("models/", ModelListAPIView.as_view(), name="model_list"),
]

urlpatterns.extend(router.urls)
