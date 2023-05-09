from urllib import request
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.views import APIView

from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
)
from cars.models import Brand, Model, Car, CarImage
from rest_framework_simplejwt.authentication import JWTAuthentication
from cars.filters import CarFilter, ModelFilter


from cars.serializers import (
    BrandSerializer,
    ModelSerializer,
    CarSerializer,
    CarCreateSerializer,
)


class BrandListAPIView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "headquarters_country"]


class ModelListAPIView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Model.objects.all()
    serializer_class = ModelSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = ModelFilter


class CarListAllAPIView(ListAPIView):
    queryset = Car.objects.all().select_related("brand", "model")
    serializer_class = CarSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = CarFilter


class CarListCreateAPIView(ListCreateAPIView):
    queryset = Car.objects.filter(is_on_sale=True).select_related("brand", "model")
    serializer_class = CarSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend]
    filterset_class = CarFilter

    def post(self, *args, **kwargs):
        request_data = self.request.data.copy()
        request_data["user"] = self.request.user.pk

        serializer = CarCreateSerializer(data=request_data)

        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
        return Response(CarSerializer(instance).data)
