from django.urls import path
from user import views

urlpatterns = [
    path('register/', views.register, name = 'register'),
    path('login/',views.login, name = 'login'),
    path('logout/',views.logout, name = 'logout'),
    path('update/', views.update, name = 'update')
]
