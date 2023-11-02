from cars.filters import CarFilter
from cars.models import Brand, Car, Model
from cars.permissions import IsCarOwner
from cars.serializers import (BrandSerializer, CarCreateUpdateSerializer,
                              CarSerializer, ModelSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import (SAFE_METHODS, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet


class BrandListAPIView(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ModelListAPIView(ListAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer


class CarViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CarFilter

    ordering_fields = ["price", "year", "created_at"]
    ordering = ["-created_at"]

    queryset = (
        Car.objects.available()
        .select_related(
            "brand",
            "model",
            "user",
        )
        .prefetch_related(
            "images",
            "comments",
        )
    )

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return CarSerializer
        else:
            return CarCreateUpdateSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticated, IsCarOwner]

        return super().get_permissions()

    @extend_schema(request=CarCreateUpdateSerializer, responses=CarSerializer)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(
            CarSerializer(instance, context=self.get_serializer_context()).data
        )

    @extend_schema(request=CarCreateUpdateSerializer, responses=CarSerializer)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response(
            CarSerializer(instance, context=self.get_serializer_context()).data
        )
