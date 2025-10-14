from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display=('username','phone_number','employee_id','is_staff','is_active')
    
    #Add these fields to the user detail/edit form
    fieldsets=UserAdmin.fieldsets+(
        (None,{'fields':('phone_number','employee_id')}),
    )
    #add these field to the use detail/edit form
    add_fieldsets=UserAdmin.add_fieldsets +(
        (None,{'fields':('phone_number','employee_id')}),
    )
    
 
# Register your models here.
