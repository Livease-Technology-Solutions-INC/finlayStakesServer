from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from .models import OtpToken
from django.core.mail import send_mail
from django.utils import timezone


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_token(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        # Check if an OTP token already exists for the user
        existing_token = OtpToken.objects.filter(user=instance).exists()
        if not existing_token:
            otp = OtpToken.objects.create(
                user=instance,
                otp_expires_at=timezone.now() + timezone.timedelta(minutes=5),
            )
            instance.is_active = False
            instance.save()

            # email credentials
            subject = "Email Verification"
            message = f"Hi {instance.username}, your OTP is {otp.otp_code}"

            sender_email = "FinlayStakes@FinlayStakes.com"
            receiver_email = instance.email

            # send email
            send_mail(
                subject,
                message,
                sender_email,
                [receiver_email],
                fail_silently=False,
            )
