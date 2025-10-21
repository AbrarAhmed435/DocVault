from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/',PhoneTokenObtainPairView.as_view(),name='get_token'),
    path('token/refresh/',TokenRefreshView.as_view(),name="refresh"),
    path('addpatients/',PatientListCreateView.as_view(),name='patients'),
    path('patients/<int:patient_id>/visits/',VisitListCreateView.as_view(),name='patient_visites'),
    path('patients/<int:pk>/',PatientDeleteUpdateView.as_view(),name="patient_detail"),
    path('delete/patient/visit/<int:pk>/',VisitRetrieveUpdateDeleteView.as_view(),name="delete_visit"),
    path("askai/",prompt_ai,name="ask_ai"),
]
