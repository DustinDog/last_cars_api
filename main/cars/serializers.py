from rest_framework import serializers
from cars.models import Brand, Model, Car, CarImage
from core.serializers import UserSerializer


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "headquarters_country"]


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ["id", "name", "body_style", "brand"]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ("id", "image")


class CarSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    model = ModelSerializer()
    user = UserSerializer()
    images = ImageSerializer(read_only=True, many=True)

    class Meta:
        model = Car
        fields = [
            "id",
            "year",
            "condition",
            "is_on_sale",
            "title",
            "description",
            "brand",
            "model",
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


class CarCreateUpdateSerializer(serializers.ModelSerializer):
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
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
