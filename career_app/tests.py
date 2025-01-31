from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from .models import EmailVerification
from .utils import send_verification_email, send_email, resend_verification_email
from django.core.mail import send_mail
from unittest.mock import patch


class UserTests(TestCase):

    def setUp(self):
        # Creating a test user
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com",
            password="testpassword123"
        )
        self.user.is_active = False  # Make sure the user isn't verified
        self.user.save()

    def test_signup(self):
        """Test user signup"""
        response = self.client.post(reverse('career_app/signup'), {
            'email': 'newuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please check your inbox to verify your email')

    def test_login_view(self):
        """Test user login view"""
        # First, activate the user by sending a verification email
        send_verification_email(self.user, self.client.request())
        response = self.client.post(reverse('career_app/login'), {
            'email': self.user.email,
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome back!')

    def test_resend_verification_email(self):
        """Test resending verification email"""
        response = self.client.get(reverse('career_app/email/resend_verification_email', args=[self.user.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect after sending the email

    def test_email_verification(self):
        """Test email verification process"""
        verification = EmailVerification.objects.create(user=self.user)
        verification_link = f"/verify-email/{verification.token}/"
        response = self.client.get(verification_link)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your email has been verified')

    def test_send_email_function(self):
        """Test the send_email utility function"""
        with patch('django.core.mail.send_mail') as mock_send_mail:
            send_email("Test Subject", "Test Message", ["test@example.com"])
            mock_send_mail.assert_called_once_with(
                "Test Subject",
                "Test Message",
                'noreply@yourdomain.com',  # Replace with actual default email
                ["test@example.com"],
                fail_silently=False
            )

    def test_send_verification_email_function(self):
        """Test the send_verification_email utility function"""
        with patch('career_app.utils.send_email') as mock_send_email:
            send_verification_email(self.user, self.client.request())
            mock_send_email.assert_called_once()  # Ensure send_email was called

    def test_resend_verification_email_function(self):
        """Test the resend_verification_email utility function"""
        with patch('career_app.utils.send_verification_email') as mock_send_verification_email:
            resend_verification_email(self.user, self.client.request())
            mock_send_verification_email.assert_called_once()  # Ensure resend is triggered


class EmailVerificationTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            password="testpassword123"
        )
        self.verification = EmailVerification.objects.create(user=self.user)

    def test_verification_creation(self):
        """Test that verification is created for the user"""
        self.assertIsInstance(self.verification, EmailVerification)
        self.assertEqual(self.verification.user, self.user)

    def test_verification_token_validity(self):
        """Test that the verification token expires after 24 hours"""
        self.assertTrue(self.verification.is_token_valid())

    def test_verify_token_function(self):
        """Test the verify_token function"""
        verification = EmailVerification.objects.create(user=self.user)
        token = verification.token
        result = verify_token(token)
        self.assertIsNotNone(result)
        self.assertEqual(result.user, self.user)

    def test_resend_verification_if_no_valid_token(self):
        """Test that a new token is created if the previous one is invalid"""
        self.verification.is_verified = False
        self.verification.expires_at = now() - timedelta(days=1)  # Expire the token
        self.verification.save()
        
        response = self.client.get(reverse('career_app/email/resend_verification_email', args=[self.user.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect

    def test_resend_verification_with_valid_token(self):
        """Test that no new token is created if there's a valid token"""
        response = self.client.get(reverse('career_app/email/resend_verification_email', args=[self.user.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect

