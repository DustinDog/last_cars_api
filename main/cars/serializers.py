from rest_framework import serializers
from cars.models import Brand, Model, Car, CarImage


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = "__all__"


"""Serializer for car itself"""


class CarSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    model = ModelSerializer()

    class Meta:
        model = Car
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ("car", "image")


"""serializer for creating car"""


class CarCreateSerializer(serializers.ModelSerializer):
    images = ImageSerializer(read_only=True, many=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
    )

    class Meta:
        model = Car
        fields = [
            "title",
            "description",
            "brand",
            "model",
            "is_on_sale",
            "engine",
            "price",
            "mileage",
            "exterior_color",
            "interior_color",
            "fuel_type",
            "transmission",
            "images",
            "uploaded_images",
            "user",
        ]

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        if len(uploaded_images) < 3:
            raise serializers.ValidationError(
                f"You uploaded {len(uploaded_images)} images.Please upload at least 3 images."
            )
        validated_data["is_on_sale"] = True

        car = Car.objects.create(**validated_data)
        for image in uploaded_images:
            CarImage.objects.create(car=car, image=image)
        return car
