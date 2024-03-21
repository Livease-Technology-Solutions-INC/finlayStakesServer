from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from .models import OtpToken
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .models import MyUser  # assuming MyUser is your custom user model
from .utils import PasswordResetEmailSender

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_token(sender, instance, created, **kwargs):
   if created and not instance.is_superuser:
    # Check if an OTP token already exists for the user
    existing_token = OtpToken.objects.filter(user=instance).first()
    if not existing_token:
        otp = OtpToken.objects.create(
            user=instance,
            otp_expires_at=timezone.now() + timezone.timedelta(minutes=5),
        )
        instance.is_active = False
        instance.save()

        # Send email with newly generated OTP code
        subject = "Email Verification"
        message = f"Hi {instance.username}, your OTP is {otp.otp_code}"
    else:
        # Resend existing OTP code
        subject = "Email Verification"
        message = f"Hi {instance.username}, your OTP is {existing_token.otp_code}"

    sender_email = "princewill835@gmail.com"
    receiver_email = instance.email

    # Send email
    send_mail(
        subject,
        message,
        sender_email,
        [receiver_email],
        fail_silently=False,
    )

@receiver(post_save, sender=MyUser)
def send_password_reset_email(sender, instance, created, **kwargs):
    if created:
        PasswordResetEmailSender.send_password_reset_email(instance)