from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import status
from core.serializers import UserCreateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)

        refresh = RefreshToken.for_user(instance)
        tokens = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return Response(
            {**serializer.data, **tokens},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class ProtectedView(APIView):
    authentication_classes = [JWTAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = {"result": True}
        return Response(data)


class Healthcheck(APIView):
    def get(self, request):
        return Response([], status=status.HTTP_200_OK)
