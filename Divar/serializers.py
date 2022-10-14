from rest_framework import serializers
from django.contrib.auth import get_user_model

from Auth import models


User = get_user_model()


class IPSerializer(serializers.ModelSerializer):
    """
        IP Serializer
    """
    class Meta(object):
        """
            Meta
        """
        model = models.UserRequest
        fields = "__all__"


class RequestSerializer(serializers.Serializer):
    """
        Request Serializer
    """
    query = serializers.CharField(required=True)
    limit = serializers.IntegerField(default=24)
    has_photo = serializers.BooleanField(default=False)
    urgent = serializers.BooleanField(default=False)
