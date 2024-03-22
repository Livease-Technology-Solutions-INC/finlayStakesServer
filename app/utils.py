from base64 import urlsafe_b64encode
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode


class PasswordResetEmailSender:
    @staticmethod
    def send_password_reset_email(user):
        # Generate a password reset token
        uid = urlsafe_b64encode(force_bytes(user.id))
        token = default_token_generator.make_token(user)

        # Construct the reset link
        reset_link = (
            f" http://127.0.0.1:8000/app/reset-password/{uid.decode()}/{token}/"
        )

        # Render the email template
        email_subject = "Password Reset Request"
        email_message = f"""
        Subject: {email_subject}

        Hello,

        You recently requested to reset your password for your account.

        Please click on the following link to reset your password:

        {reset_link}

        If you didn't request a password reset, you can ignore this email.

        Thanks,
        William
        """

        # Send the email
        send_mail(
            email_subject,
            email_message,
            "princewill835@gmail.com",
            [user.email],
        )
