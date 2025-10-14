from django.shortcuts import render
from rest_framework import generics
from .serializers import RegisterSerializer,PhoneTokenObtainPairSerializer
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
            {"message":f"Docter with Employeeid-{user.employee_id} created"},status=status.HTTP_201_CREATED
        )

class PhoneTokenObtainPairView(TokenObtainPairView):
    serializer_class=PhoneTokenObtainPairSerializer

    


# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class=MyTokenObtainPairSerializer