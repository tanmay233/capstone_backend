from django.urls import path
from . import views

urlpatterns = [
    path('postquestion/', views.post_question, name = 'post_question'),
    path('updatequestion/', views.update_question, name = 'update_question'),
    path('deletequestion/', views.delete_question, name = 'deletequestion')
]
