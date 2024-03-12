from django.contrib import admin
from app.models import CustomUser, PersonalDetails
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email']
    
class PersonalDetailsAdmin(admin.ModelAdmin):
    list_editable = ['contact_number', 'name']
    list_display = ['user', 'name', 'contact_number']
    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(PersonalDetails, PersonalDetailsAdmin)