from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,required=True,validators=[validate_password])
    confirm_password=serializers.CharField(write_only=True,required=True)
    
    class Meta:
        mode=CustomUser
        fields=('first_name','last_name','username','phone_number','employee_id','password','confirm_password')
    
    def validate(self,attrs):
        if attrs['password'] !=attrs['confirm_passord']:
    