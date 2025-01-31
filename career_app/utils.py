from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from .models import EmailVerification, CustomUser
from datetime import timedelta
import logging
import secrets  # More secure than uuid4()
logger = logging.getLogger(__name__)
import uuid  # Ensure uuid is imported

# Utility function to send an email with both HTML and text fallback
def send_email(subject, template_name, context, recipient_list):
    """
    Sends an email with both HTML and plain text versions.
    """
    try:
        message_text = render_to_string(template_name + ".txt", context)
        message_html = render_to_string(template_name + ".html", context)

        email = EmailMultiAlternatives(
            subject=subject,
            body=message_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipient_list,
        )
        email.attach_alternative(message_html, "text/html")
        email.send(fail_silently=False)  # Set to True in production

        logger.info(f"Email sent successfully to {', '.join(recipient_list)}")
    except Exception as e:
        logger.error(f"Error sending email to {', '.join(recipient_list)}: {e}")
        raise


# Function to send a verification email to a user
def send_verification_email(user, request):
    """
    Sends a verification email to the user with a unique token.
    """
    with transaction.atomic():
        # Delete old verification entries
        EmailVerification.objects.filter(user=user).delete()

        # Create a new email verification entry with a valid UUID
        verification = EmailVerification.objects.create(
            user=user,
            token=str(uuid.uuid4()),  # Convert UUID to a string format
            expires_at=now() + timedelta(hours=24)
        )

    verification_link = f"https://{get_current_site(request).domain}{reverse('verify_email', args=[verification.token])}"

    # Send email
    send_email(
        subject="Please verify your email",
        template_name='career_app/email/verify_email',
        context={'user': user, 'verification_link': verification_link},
        recipient_list=[user.email],
    )


# Function to verify a token
def verify_token(token):
    """
    Verifies the token and marks the email as verified if valid.
    """
    try:
        verification = EmailVerification.objects.get(token=token)

        if not verification.is_token_valid():
            logger.warning(f"Token {token} has expired.")
            return None  # Token expired

        # Mark the user as verified
        verification.user.is_verified = True
        verification.user.save()
        verification.delete()

        logger.info(f"Email verified successfully for {verification.user.email}")
        return verification.user

    except EmailVerification.DoesNotExist:
        logger.warning(f"Token {token} does not exist.")
        return None


# Function to resend a verification email
def resend_verification_email(user, request):
    """
    Resends a verification email by generating a new token.
    """
    return send_verification_email(user, request)


# Function to send a password reset email
def send_password_reset_email(user, request):
    """
    Sends a password reset email.
    """
    with transaction.atomic():
        # Try to get an existing valid reset token
        verification = EmailVerification.objects.filter(user=user, expires_at__gt=now(), is_verified=False).first()

        if not verification:
            token = str(uuid.uuid4())  # Generate a proper UUID
            verification = EmailVerification.objects.create(
            user=user,
            token=token,
            expires_at=now() + timedelta(hours=1)  # Reset token valid for 1 hour
        )


    reset_link = f"https://{get_current_site(request).domain}{reverse('reset_password', args=[verification.token])}"

    # Send email
    send_email(
        subject="Password Reset Request",
        template_name='career_app/email/reset_password_email',
        context={'user': user, 'reset_link': reset_link},
        recipient_list=[user.email],
    )
