from django.urls import path
from .views import filter_view

urlpatterns = [
    path("filter/", filter_view, name="filter"),
]
