from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.decorators import action


from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    SAFE_METHODS,
)

from cars.permissions import IsCarOwner
from cars.models import Brand, Model, Car
from cars.filters import CarFilter, ModelFilter


from cars.serializers import (
    BrandSerializer,
    ModelSerializer,
    CarSerializer,
    CarCreateUpdateSerializer,
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


class CarViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarFilter
    queryset = Car.objects.available().select_related("brand", "model")

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
    def create(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(CarSerializer(instance).data)

    @extend_schema(request=CarCreateUpdateSerializer, responses=CarSerializer)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response(CarSerializer(instance).data)


class FavouritesViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Car.objects.available()
    serializer_class = CarSerializer

    @action(methods=["GET"], detail=True, url_path="add")
    def add_to_favourites(self, request, *args, **kwargs):
        car = self.get_object()

        user = request.user
        if car not in user.favourite_cars.all():
            user.favourite_cars.add(car)
            return Response(
                {"message": "Car added successfully"}, status=status.HTTP_200_OK
            )

        return Response(
            {"message": "Car already in favourites"}, status=status.HTTP_400_BAD_REQUEST
        )

    @action(methods=["GET"], detail=True, url_path="remove")
    def remove_from_favourites(self, request, *args, **kwargs):
        car = self.get_object()
        user = request.user

        if car in user.favourite_cars.all():
            user.favourite_cars.remove(car)
            return Response(
                {"message": "Successfully removed car from favourites"},
                status=status.HTTP_204_NO_CONTENT,
            )

        return Response(
            {"message": "There is no such car in favourites"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(methods=["GET"], detail=False, url_path="list")
    def list_of_favourites(self, request, *args, **kwargs):
        user = request.user
        favourites = user.favourite_cars.all()
        serializer = self.get_serializer(favourites, many=True)
        return Response(serializer.data)
