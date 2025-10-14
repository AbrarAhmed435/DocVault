from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,PermissionsMixin
from django.conf import settings

class CustomUser(AbstractUser):
    phone_number=models.CharField(max_length=10,unique=True)
    employee_id=models.CharField(max_length=20,unique=True)
    
    def __str__(self):
        return f"{self.username} ({self.employee_id})"
    

class Patient(models.Model):
    doctor=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patients'
    )
    name=models.CharField(max_length=100)
    age=models.PositiveIntegerField()
    gender_choices=[('M','Male'),('F','Female'),('O','Other')]
    gender=models.CharField(max_length=1,choices=gender_choices)
    weight_kg=models.FloatField()
    height_cm=models.FloatField()
    
    def __str__(self):
        return f"{self.name} ({self.id})"

class Visit(models.Model):
    patient=models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='visites'
    )
    visit_no=models.PositiveIntegerField()
    diagnosis=models.TextField()
    treatment=models.TextField()
    test=models.TextField(blank=True,null=True)
    date_created=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together=('patient','visit_no')
        ordering=['visit_no']
        
    def save(self,*args, **kwargs):
        if not self.visit_no:
            #Auto increment visit_no per patient
            last_visit=Visit.objects.filter(patient=self.patient).order_by('-visit_no').first()
            self.visit_no=last_visit.visit_no+1 if last_visit else 1
        super().save(*args,**kwargs)
        
    def __str__(self):
        return f"Visit {self.visit_no} - {self.patient.name}"
        