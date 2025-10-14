from django.shortcuts import render
from rest_framework import generics,permissions
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterView(generics.CreateAPIView):
    serializer_class=RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        
        return Response(
            {"message":f"Doctor with Employeeid-{user.employee_id} created"},status=status.HTTP_201_CREATED
        )

class PhoneTokenObtainPairView(TokenObtainPairView):
    serializer_class=PhoneTokenObtainPairSerializer

    
class PatientListCreateView(generics.ListCreateAPIView):
    serializer_class=PatientSerializer
    permission_classes=[permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Patient.objects.filter(doctor=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)


class VisitListCreateView(generics.ListCreateAPIView):
    serializer_class=VisitSerializer
    permission_classes=[permissions.IsAuthenticated]
    
    def get_queryset(self):
        patient_id=self.kwargs.get('patient_id')
        return Visit.objects.filter(patient_id=patient_id)
    
    def perform_create(self, serializer):
        patient_id=self.kwargs.get('patient_id')
        patient=Patient.objects.get(id=patient_id,doctor=self.request.user)
        serializer.save(patient=patient)

        
# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class=MyTokenObtainPairSerializer