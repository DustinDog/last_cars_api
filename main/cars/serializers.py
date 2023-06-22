import base64
import uuid

import six
from cars.models import Brand, Car, CarImage, Model
from comments.serializers import RetrieveCommentSerializer
from core.serializers import UserSerializer
from django.core.files.base import ContentFile
from rest_framework import serializers


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ["id", "name", "body_style", "brand"]


class CarBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "headquarters_country"]


class BrandSerializer(serializers.ModelSerializer):
    models = ModelSerializer(many=True)

    class Meta:
        model = Brand
        fields = ["id", "name", "headquarters_country", "models"]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ("id", "image")


class CarSerializer(serializers.ModelSerializer):
    comments = RetrieveCommentSerializer(read_only=True, many=True)
    is_favourite = serializers.SerializerMethodField()
    brand = CarBrandSerializer()
    model = ModelSerializer()
    user = UserSerializer()
    images = ImageSerializer(read_only=True, many=True)

    class Meta:
        model = Car
        fields = [
            "id",
            "comments",
            "brand",
            "model",
            "created_at",
            "updated_at",
            "is_favourite",
            "year",
            "condition",
            "is_on_sale",
            "title",
            "description",
            "user",
            "engine",
            "price",
            "mileage",
            "exterior_color",
            "interior_color",
            "fuel_type",
            "transmission",
            "images",
        ]

    def get_is_favourite(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return obj in user.favourite_cars.all()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, six.string_types):
            if "data:" in data and ";base64," in data:
                header, data = data.split(";base64,")

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail("invalid_image")

            file_name = str(uuid.uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (
                file_name,
                file_extension,
            )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class CarCreateUpdateSerializer(serializers.ModelSerializer):
    uploaded_images = serializers.ListField(
        child=Base64ImageField(max_length=None, use_url=True),
        write_only=True,
    )

    class Meta:
        model = Car
        fields = [
            "title",
            "year",
            "condition",
            "description",
            "brand",
            "model",
            "engine",
            "price",
            "mileage",
            "exterior_color",
            "interior_color",
            "fuel_type",
            "transmission",
            "uploaded_images",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        uploaded_images = validated_data.pop("uploaded_images")
        if len(uploaded_images) < 3:
            raise serializers.ValidationError(
                f"You uploaded {len(uploaded_images)} images.Please upload at least 3 images."
            )
        validated_data["is_on_sale"] = False

        car = Car.objects.create(**validated_data, user=user)
        for image in uploaded_images:
            CarImage.objects.create(car=car, image=image)
        return car
