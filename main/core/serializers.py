from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
        )


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirmed_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["password"] != data["confirmed_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop("confirmed_password")
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()

        return user

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "confirmed_password",
            "password",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "favourite_cars",
        )


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "phone_number",
        )


class PasswordUpdateSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_confirmed_password = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        old_password = validated_data.get("old_password")
        new_password = validated_data.get("new_password")
        new_confirmed_password = validated_data.get("new_confirmed_password")

        if not instance.check_password(old_password):
            raise serializers.ValidationError("Incorrect old password.")

        if new_password != new_confirmed_password:
            raise serializers.ValidationError("New password fields do not match.")

        instance.set_password(new_password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = (
            "old_password",
            "new_password",
            "new_confirmed_password",
        )
