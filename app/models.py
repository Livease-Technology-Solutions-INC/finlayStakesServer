from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver
# models
class CustomUser(AbstractUser):
    email = models.EmailField(max_length=250, unique=True)
    profile_image = models.ImageField(upload_to="profile", blank=True, null=True)
    phone_number = PhoneNumberField(blank=True)
    is_google = models.BooleanField(default=False)
    is_facebook = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    def __str__(self):
        return self.email

class PersonalDetails(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='personal_details'
    )
    name = models.CharField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    marital_status = models.CharField(max_length=20, blank=True)
    contact_number = PhoneNumberField(blank=True)
    country_of_residence = models.CharField(blank=True, null=True)
    nationality = models.CharField(blank=True, null=True)
    address = models.CharField(blank=True, null=True)
    medical_history = models.CharField(blank=True, null=True)
    smoker = models.BooleanField(default=False, null=True)

    def save(self, *args, **kwargs):
        # Calculate age from date of birth
        if self.date_of_birth:
            today = date.today()
            self.age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        super().save(*args, **kwargs)
        
def create_personal_details(sender, instance, created, **kwargs):
    if created: 
        PersonalDetails.objects.create(user=instance)
def save_personal_details(sender, instance, **kwargs):
    instance.personal_details.save()

post_save.connect(create_personal_details, sender=CustomUser)
post_save.connect(save_personal_details, sender=CustomUser)
    
