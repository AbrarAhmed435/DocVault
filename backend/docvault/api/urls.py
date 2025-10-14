from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/',PhoneTokenObtainPairView.as_view(),name='get_token'),
    path('token/refresh/',TokenRefreshView.as_view(),name="refresh"),
]
