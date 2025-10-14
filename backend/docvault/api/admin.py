from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

class PatientInline(admin.TabularInline):
    model = Patient
    extra = 0
    fields = ('name', 'age', 'gender', 'weight_kg', 'height_cm')
    readonly_fields = ()
    show_change_link = True 
    
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
    inlines = [PatientInline]

    # Optional: only show patients belonging to the user
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.id)

class VisitInline(admin.TabularInline):
    model = Visit
    extra = 0  # Don't show empty extra rows
    readonly_fields = ('visit_no', 'date_created')  # Auto fields
 
# Register your models here.
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'weight_kg', 'height_cm', 'doctor')
    search_fields = ('name', 'doctor__username', 'doctor__employee_id')
    list_filter = ('gender',)
    inlines = [VisitInline]

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('patient', 'visit_no', 'diagnosis', 'treatment', 'test', 'date_created')
    list_filter = ('date_created',)
    search_fields = ('patient__name', 'diagnosis')


