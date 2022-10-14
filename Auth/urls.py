from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from . import views

urlpatterns = [
    path("register", views.UserRegister.as_view()),
    path("profile", views.UserProfile.as_view()),
    path("token", TokenObtainPairView.as_view()),
    path("token/refresh", TokenRefreshView.as_view()),
    path("token/verify", TokenVerifyView.as_view()),
]
