from rest_framework.permissions import BasePermission
from cars.models import Car


class IsCarOwner(BasePermission):
    def has_permission(self, request, view):
        car = Car.objects.get(pk=view.kwargs.get("pk"))
        return car.user == request.user
