from cars.models import Car
from cars.serializers import CarSerializer
from core.send_email import send_email_varification
from core.serializers import (
    EmailUpdateSerializer,
    PasswordUpdateSerializer,
    UpdateUserProfileSerializer,
    UserCreateSerializer,
    UserProfileSerializer,
)
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from rest_framework import generics, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()


class ActivateUserView(APIView):
    def get(self, request):
        user = User.objects.get(pk=request.GET.get("user_id"))

        if not default_token_generator.check_token(
            user, request.GET.get("confirmation_token")
        ):
            return Response(
                {
                    "message": "Token is invalid or expired. Please request another confirmation email by signing in."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.email_verified = True

        user.save()
        return Response({"message": "Email successfully confirmed"})


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)

        activation_link = request.build_absolute_uri(reverse("activate"))
        send_email_varification(activation_link, instance)

        refresh = RefreshToken.for_user(instance)
        tokens = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return Response(
            {
                "message": "Check your email",
                **UserProfileSerializer(instance).data,
                **tokens,
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class Healthcheck(APIView):
    def get(self, request):
        return Response([], status=status.HTTP_200_OK)


class FavouritesViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Car.objects.available().select_related("brand", "model")
    serializer_class = CarSerializer

    @action(methods=["GET"], detail=True, url_path="add")
    def add_to_favourites(self, request, *args, **kwargs):
        car = self.get_object()

        user = request.user
        if car not in user.favourite_cars.all():
            user.add_to_favourites(car)
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
            user.remove_from_favourites(car)
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

        favourites = (
            user.favourite_cars.all()
            .select_related("brand", "model", "user")
            .prefetch_related("images")
        )

        serializer = self.get_serializer(favourites, many=True)
        return Response(serializer.data)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request):
        serializer = self.serializer_class
        return Response(serializer(request.user).data)

    def patch(self, request, *args, **kwargs):
        serializer = UpdateUserProfileSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserProfileSerializer(request.user).data)


class PasswordUpdateView(APIView):
    def put(self, request):
        serializer = PasswordUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(request.user, serializer.validated_data)
            return Response(
                {"message": "Password chenged successfully!"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailUpdateView(UpdateAPIView):
    def put(self, request, *args, **kwargs):
        serializer = EmailUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.update(request.user, request.data)

        activation_link = request.build_absolute_uri(reverse("activate"))
        send_email_varification(activation_link, instance)
        return Response({"message": "Check your email"}, status=status.HTTP_200_OK)
