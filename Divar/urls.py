from django.urls import path

from . import views

urlpatterns = [
    path("", views.SearchQueryView.as_view(), name="query-search"),
]
