import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from django.contrib.auth import get_user_model

from Auth import serializers as auth_serializer
from .utils import get_ip_address, get_items
from App.settings import SECRET_KEY
from . import serializers
from Auth import models


User = get_user_model()


class SearchQueryView(APIView):
    """
        docstring
    """

    def get_ip_object(self, user_ip: str):
        """
            Get User Object
        """
        try:
            return models.UserRequest.objects.get(user_ip=user_ip)
        except models.UserRequest.DoesNotExist:
            return None

    def get_user_object(self, mobile: int):
        """
            Get User Object
        """
        try:
            return User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            return None

    def post(self, request):
        """
            Search Items
        """

        # Input Data Validation
        request_serializer = serializers.RequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data

        # Check User Is Authorized OR NOT
        user_data = request.user
        if user_data.is_authenticated:
            user = self.get_user_object(user_data)
            if user:
                user_serializer = auth_serializer.UserSerializer(instance=user)
                user_serializer_data = user_serializer.data

                # If User's Credit Is Finished
                if not user_serializer_data["credit"]:
                    response = {
                        "message": "Increase Your CREDIT!"
                    }
                    return Response(response, status.HTTP_402_PAYMENT_REQUIRED)

                serialized_user = auth_serializer.UserSerializer(
                    instance=user,
                    data=user_serializer_data,
                    partial=True
                )
                serialized_user.is_valid(raise_exception=True)
                serialized_user.save()

                response = get_items(
                    validated_data["query"],
                    validated_data["limit"],
                    validated_data["has_photo"],
                    validated_data["urgent"]
                )

                return Response(response, status=status.HTTP_200_OK)

        # Check the User IP Address
        user_ip = get_ip_address(request)
        db_obj = self.get_ip_object(user_ip)
        if db_obj:
            print("New Request")
            if not db_obj.credit:
                message = {"message": "Limit Reached!"}
                return Response(message, status=status.HTTP_429_TOO_MANY_REQUESTS)

            new_data = {
                'id': db_obj.pk,
                'user_ip': db_obj.user_ip,
                'credit': db_obj.credit - 1
            }
            serialized_user_request = serializers.IPSerializer(
                instance=db_obj,
                data=new_data,
                partial=True
            )
            serialized_user_request.is_valid(raise_exception=True)
            serialized_user_request.save()
            return Response(
                get_items(
                    validated_data["query"],
                    validated_data["limit"],
                    validated_data["has_photo"],
                    validated_data["urgent"]
                )
            )

        # If User Is Not Authenticated
        print("1st Request")
        serialized_user_request = serializers.IPSerializer(
            data={"user_ip": user_ip}
        )
        serialized_user_request.is_valid(raise_exception=True)
        serialized_user_request.save()

        return Response(
            get_items(
                validated_data["query"],
                validated_data["limit"],
                validated_data["has_photo"],
                validated_data["urgent"]
            )
        )
