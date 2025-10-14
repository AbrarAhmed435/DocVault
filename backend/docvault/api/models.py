from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,PermissionsMixin


class CustomUser(AbstractUser):
    phone_number=models.CharField(max_length=10,unique=True)
    employee_id=models.CharField(max_length=20,unique=True)
    
    def __str__(self):
        return f"{self.username} ({self.employee_id})"
    
