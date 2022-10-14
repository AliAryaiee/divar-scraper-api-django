from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


def mobile_validator(mobile: str):
    """
        Mobile Number Validator
    """
    if len(mobile) != 11:
        raise serializers.ValidationError(
            "The Mobile Number Must Contain Exact 11 Digits!"
        )
    if not mobile.startswith("09"):
        raise serializers.ValidationError(
            "The Mobile Number Must Be Like 09xxxxxxxxx!"
        )
