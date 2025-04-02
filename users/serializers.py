import pycountry
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import CustomUser
from users.validators import validate_phone_number
from django.core.exceptions import ValidationError

User = get_user_model()

COUNTRY_CHOICES = [(c.alpha_2, c.name) for c in pycountry.countries]

class RegisterSerializer(serializers.ModelSerializer):
    country = serializers.ChoiceField(choices=COUNTRY_CHOICES)
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = ["id", "country", "phone_number", "name", "password", "confirm_password"]

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        try:
            validate_phone_number(data["phone_number"], data["country"])
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        # Create the user
        CustomUser.objects.create_user(**validated_data)
        # Return a custom dict
        return {"message": "User registered successfully!"}

    def to_representation(self, instance):
        # If instance is a dict, return it directly.
        if isinstance(instance, dict):
            return instance
        # Otherwise, fall back to the default behavior.
        return super().to_representation(instance)



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)  # Get the default token response

        user = self.user  # Get the authenticated user

        # Add custom user data to the response
        data["access_token"] = data.pop("access")  # Rename "access" to "access_token"
        data["refresh_token"] = data.pop("refresh")  # Rename "refresh" to "refresh_token"
        data["user"] = {
            "id": str(user.id),  # Ensure UUID is converted to string
            "name": user.name,
            "phoneNumber": user.phone_number,
            "solde": getattr(user, "solde", 0.00)  # Default to 0.00 if solde doesn't exist
        }

        return data