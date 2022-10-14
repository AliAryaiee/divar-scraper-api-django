from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from . import validators


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
        User Serializer
    """
    class Meta(object):
        """
            Meta
        """
        model = User
        fields = ("id", "mobile", "credit")
        extra_kwargs = {
            "mobile": {"validators": (validators.mobile_validator,)}
        }

    def update(self, instance, validated_data):
        """
            Consume (Update) User Credit
        """
        credit = validated_data.pop("credit")
        instance.credit = credit - 1
        instance.save()
        return instance


class UserRegisterSerializer(serializers.ModelSerializer):
    """
        User Register Serializer
    """
    class Meta(object):
        """
            Meta
        """
        model = User
        fields = ("mobile", "password")
        extra_kwargs = {
            "password": {"write_only": True},
            "mobile": {"validators": (validators.mobile_validator,)}
        }

    def get_user_tokens(self, user):
        """
            docstring
        """
        tokens = RefreshToken.for_user(user)
        return {
            "refresh": str(tokens),
            "access": str(tokens.access_token),
        }

    def create(self, validated_data: dict):
        """
            Overriding Create Method
        """
        return User.objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    """
        User Profile Serializer
    """
    class Meta(object):
        """
            Meta
        """
        model = User
        exclude = ["password"]
