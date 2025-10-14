from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User=get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,required=True,validators=[validate_password])
    confirm_password=serializers.CharField(write_only=True,required=True)
    
    class Meta:
        model=CustomUser
        fields=('first_name','last_name','username','phone_number','employee_id','password','confirm_password')
    
    def validate(self,attrs):
        if attrs['password'] !=attrs['confirm_password']:
            raise serializers.ValidationError({"password":"Passwords didn't match"})
        return attrs
    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user=CustomUser.objects.create_user(**validated_data)
        return user


class PhoneTokenObtainPairSerializer(serializers.Serializer):
    phone_number=serializers.CharField(label="Enter Phone Number")
    password=serializers.CharField(write_only=True)
    
    def validate(self,attrs):
        phone_number=attrs.get("phone_number")
        password=attrs.get("password")
        
        try:
            user=User.objects.get(phone_number=phone_number)
            
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid phone number or password")
        
        #Check if user is active
        if not user.is_active:
            raise serializers.ValidationError("User account is inactive")
        
        #Check if user is activate
        if not user.is_active:
            raise serializers.ValidationError("User account is inactivate")
        refresh=RefreshToken.for_user(user)
        
        return {
            "refresh":str(refresh),
            "access":str(refresh.access_token)
        }
            
class VisitSerializer(serializers.ModelSerializer):
    visit_no=serializers.IntegerField(read_only=True)
    class Meta:
        model=Visit
        fields=['id','visit_no','diagnosis','treatment','test','date_created']
        
class PatientSerializer(serializers.ModelSerializer):
    visits=VisitSerializer(many=True,read_only=True)
    
    class Meta:
        model=Patient
        fields=['id','name','age','gender','weight_kg','height_cm','visits']

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     username_field='phone_number'
    
#     @classmethod
#     def get_token(cls, user):
#         token=super().get_token(user)
#         token['employee_id']=user.employee_id
#         token['username']=user.username
#         return token