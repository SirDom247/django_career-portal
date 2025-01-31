from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()  # This will now point to 'career_app.CustomUser'


# Contact Form
class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100, 
        required=True, 
        widget=forms.TextInput(attrs={"placeholder": "Full name", "class": "contactInput"})
    )
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "contactInput"})
    )
    subject = forms.CharField(
        max_length=200, 
        required=True, 
        widget=forms.TextInput(attrs={"placeholder": "Subject", "class": "contactInput"})
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"placeholder": "Message", "class": "contactInput", "rows": 5}),
    )

    def clean_message(self):
        message = self.cleaned_data.get("message")
        if len(message) < 10:  # Ensure the message is at least 10 characters
            raise forms.ValidationError("Message is too short, please provide more details.")
        return message

 

class SignupForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        validators=[
            RegexValidator(
                regex='^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d@$!%*#?&]{8,}$',
                message="Password must be at least 8 characters long, include letters, numbers, and at least one special character."
            )
        ],
    )
    repeat_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat Password'}),
    )
    is_mentor = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-control'}),
        label="Register as a Mentor"
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')
        email = cleaned_data.get('email')

        # Check if passwords match
        if password != repeat_password:
            self.add_error('repeat_password', "Passwords do not match.")

        # Check if email is unique
        if User.objects.filter(email=email).exists():
            self.add_error('email', "This email is already in use.")

        return cleaned_data


# Login Form (using CustomUser)
class LoginForm(forms.Form):
    username_or_email = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get("username_or_email")
        password = cleaned_data.get("password")
        
        # Attempt to authenticate using username or email
        user = authenticate(username=username_or_email, password=password)
        
        if user is None:
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                raise ValidationError("Invalid username/email or password.")

        if user is None:
            raise ValidationError("Invalid username/email or password.")
        
        cleaned_data['user'] = user  
        return cleaned_data


# OTP Verification Form
class OTPVerificationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
    )
    otp = forms.RegexField(
        regex=r'^\d{6}$',  # Ensure OTP is exactly 6 digits
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter OTP'}),
    )


# Custom Password Reset Form
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254, 
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )


# Reset Password Form (using CustomUser)
class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(), label="New Password", max_length=100)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password", max_length=100)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        try:
            validate_password(new_password)
        except ValidationError as e:
            raise forms.ValidationError(f"Password is too weak: {', '.join(e.messages)}")

        return cleaned_data


# Forgot Password Form
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email to reset password'})
    )
