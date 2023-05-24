from rest_framework import generics, permissions

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from core.serializers import UserCreateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from cars.models import Car
from cars.serializers import CarSerializer
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
from core.send_email import send_email_varification

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
            {"message": "Check your email", **serializer.data, **tokens},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class Healthcheck(APIView):
    def get(self, request):
        return Response([], status=status.HTTP_200_OK)


class MyListingsViewSet(ReadOnlyModelViewSet):
    queryset = Car.objects.all().select_related("brand", "model")
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset
