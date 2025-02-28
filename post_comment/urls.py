from django.urls import path
from . import views

urlpatterns = [
    path("postcomment/", views.post_comment, name = 'add_comment')
]
