from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, DestroyAPIView, ListCreateAPIView

from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from cars.permissions import IsCarOwner
from cars.models import Brand, Model, Car
from rest_framework_simplejwt.authentication import JWTAuthentication
from cars.filters import CarFilter, ModelFilter


from cars.serializers import (
    BrandSerializer,
    ModelSerializer,
    CarSerializer,
    CarCreateSerializer,
)


class BrandListAPIView(ListAPIView):
    permission_classes = []

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "headquarters_country"]


class ModelListAPIView(ListAPIView):
    permission_classes = []

    queryset = Model.objects.all()
    serializer_class = ModelSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = ModelFilter


class CarListCreateAPIView(ListCreateAPIView):
    queryset = Car.objects.available().select_related("brand", "model")
    serializer_class = CarSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend]
    filterset_class = CarFilter

    @extend_schema(request=CarCreateSerializer, responses=CarSerializer)
    def post(self, *args, **kwargs):
        serializer = CarCreateSerializer(
            data=self.request.data, context={"request": self.request}
        )
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()
        return Response(CarSerializer(instance).data)


class DeleteCarByIdAPIView(DestroyAPIView):
    queryset = Car.objects.all()
    permission_classes = [IsAuthenticated, IsCarOwner]
