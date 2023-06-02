from rest_framework import serializers
from cars.models import Brand, Model, Car, CarImage
from core.serializers import UserSerializer


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
    is_favourite = serializers.SerializerMethodField()
    brand = CarBrandSerializer()
    model = ModelSerializer()
    user = UserSerializer()
    images = ImageSerializer(read_only=True, many=True)

    class Meta:
        model = Car
        fields = [
            "id",
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
