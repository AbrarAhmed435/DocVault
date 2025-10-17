from django.shortcuts import render
from rest_framework import generics,permissions
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterView(generics.CreateAPIView):
    serializer_class=RegisterSerializer
    authentication_classes=[]
    permission_classes=[permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        
        return Response(
            {"message":f"Doctor with Employeeid-{user.employee_id} created"},status=status.HTTP_201_CREATED
        )
# class RegisterView(generics.CreateAPIView):
#     serializer_class = RegisterSerializer
#     authentication_classes = []
#     permission_classes = [permissions.AllowAny]
    
#     def create(self, request, *args, **kwargs):
#         print("=== REGISTER VIEW REACHED ===")
#         print("Request data:", request.data)
        
#         serializer = self.get_serializer(data=request.data)
        
#         print("=== BEFORE VALIDATION ===")
#         if not serializer.is_valid():
#             print("=== VALIDATION ERRORS ===")
#             print("Errors:", serializer.errors)
#             print("Error details:", dict(serializer.errors))  # Fixed this line
#             # This will raise the exception and return 400
#             serializer.is_valid(raise_exception=True)
        
#         print("=== AFTER VALIDATION - SAVING ===")
#         user = serializer.save()
#         print("=== USER CREATED ===")
        
#         return Response(
#             {"message": f"Doctor with Employeeid-{user.employee_id} created"}, 
#             status=status.HTTP_201_CREATED
#         )

class PhoneTokenObtainPairView(TokenObtainPairView):
    serializer_class=PhoneTokenObtainPairSerializer

    
class PatientListCreateView(generics.ListCreateAPIView):
    serializer_class=PatientSerializer
    permission_classes=[permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Patient.objects.filter(doctor=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)


class PatientDeleteUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Patient.objects.all()
    serializer_class=PatientSerializer
    permission_classes=[permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Ensuere docter can only access their own patients
        
        return Patient.objects.filter(doctor=self.request.user)

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