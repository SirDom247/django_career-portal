from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout, update_session_auth_hash
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.timezone import now
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .models import (
    EmailVerification,
    Contact,
    LMScourse,
    CourseMaterial,
    PasswordReset,
    Mentor,
    MentorSession,
)
from .forms import SignupForm, LoginForm, ContactForm, ResetPasswordForm
from .utils import send_verification_email
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
import requests
from django.conf import settings

from django.db import transaction, IntegrityError
 

User = get_user_model()

def home(request):
    return render(request, 'career_app/home.html')

def about(request):
    return render(request, 'career_app/aboutus.html')

 
 
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import ContactMessage
           
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save message in the database
            contact_message = ContactMessage(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message']
            )
            contact_message.save()

            # Admin email details
            from_email = "no-reply@fcetomokucsc.ng"   
            admin_email = "admin@fcetomokucsc.ng" 
            user_email = form.cleaned_data['email']  

            # Email to Admin
            admin_email_body = f"""
            You have received a new contact form submission:

            Name: {form.cleaned_data['name']}
            Email: {form.cleaned_data['email']}
            Subject: {form.cleaned_data['subject']}
            Message:
            {form.cleaned_data['message']}

            You can reply directly to this email to respond to the sender.
            """
            admin_email_message = EmailMessage(
                subject=f"New Contact Form Submission: {form.cleaned_data['subject']}",
                body=admin_email_body,
                from_email=from_email, 
                to=[admin_email],  
                reply_to=[user_email]   
            )
            admin_email_message.send(fail_silently=False)

            # Acknowledgment Email to User
            user_email_body = f"""
            Hello {form.cleaned_data['name']},

            Thank you for reaching out to us. We have received your message and will get back to you soon.

            Below is a copy of your submission:
            -----------------------------------
            Subject: {form.cleaned_data['subject']}
            Message:
            {form.cleaned_data['message']}
            -----------------------------------

            Regards,  
            Career Service Centre  
            FCE(T) Omoku, Rivers State, Nigeria  
            """
            user_email_message = EmailMessage(
                subject="Thank You for Contacting Us!",
                body=user_email_body,
                from_email=from_email,
                to=[user_email]
            )
            user_email_message.send(fail_silently=False)

            # Display success message
            # messages.success(request, "Your message has been sent successfully. We will get back to you soon!")
            return redirect('career_app/success')
           

        else:
            messages.error(request, "There was an error with your submission. Please correct the form and try again.")
            return render(request, 'career_app/contact.html', {'form': form})

    else:
        form = ContactForm()

    locations = [
        {
            "name": "Career Service Centre",
            "phone": "+23480FCETOMOKUCSC",
            "address": "FCE(T) Omoku, Rivers State, Nigeria",
            "email": "info@fcetomokucsc.ng"
        }
    ]
    
    return render(request, "career_app/contact.html", {"form": form, "locations": locations})



from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignupForm
from .utils import send_verification_email
from .models import EmailVerification

User = get_user_model()

import logging

logger = logging.getLogger(__name__)

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            try:
                with transaction.atomic():
                    # Prevent duplicate email signups
                    if User.objects.filter(email=email).exists():
                        messages.error(request, "An account with this email already exists.")
                        return redirect("career_app/signup")

                    # Create the user
                    user = User.objects.create_user(
                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name,
                    )
                    user.is_active = False  # Require email verification before activation
                    user.save()

                    # Ensure a unique email verification entry
                    email_verification, created = EmailVerification.objects.get_or_create(user=user)
                    
                    if created:  # Send email only if verification entry is new
                        send_verification_email(user, request)
                    
                    messages.success(request, "Account created. Please check your email for verification.")
                    return redirect("career_app/login")

            except IntegrityError as e:
                logger.error(f"IntegrityError during signup: {e}")
                messages.error(request, "A database error occurred. Please try again.")
            except Exception as e:
                logger.error(f"Unexpected error during signup: {e}")
                messages.error(request, "An unexpected error occurred. Please contact support.")

    else:
        form = SignupForm()

    return render(request, "career_app/signup.html", {"form": form})


# Login view
def login_view(request):
    if request.user.is_authenticated:
        return redirect('career_app/lms')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            auth_login(request, user)
            messages.success(request, 'You are now logged in!')
            return redirect('career_app/lms')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()

    return render(request, 'career_app/login.html', {'form': form})


# Logout view
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('career_app/home')

from django.urls import reverse

# Verify email
def verify_email(request, token):
    verification = get_object_or_404(EmailVerification, token=token)

    if verification.is_token_valid():
        user = verification.user
        user.is_active = True
        user.save()
        verification.is_verified = True
        verification.save()
        messages.success(request, "Your email has been successfully verified.")
        return redirect("career_app/login")
    else:
        messages.error(request, "This verification link has expired.")
        return render(request, 'career_app/error.html', {"message": "Verification link expired"})

 

# Resend Verification Email view
def resend_verification_email(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('career_app/login')
    
    if user.is_active:
        messages.info(request, 'This user is already verified.')
        return redirect('career_app/login')

    try:
        # Generate a new verification token and send it
        verification = EmailVerification.objects.create(user=user)
        send_verification_email(user, request)
        messages.success(request, 'Verification email sent successfully. Please check your inbox.')
    except Exception as e:
        messages.error(request, f'Error sending verification email: {e}')

    return redirect('career_app/login')


# Forgot password
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            password_reset = PasswordReset.objects.create(user=user)
            reset_url = reverse('reset-password', kwargs={'reset_id': password_reset.reset_id})
            full_reset_url = f"{request.scheme}://{request.get_host()}{reset_url}"

            send_mail(
                'Password Reset Request',
                f'Reset your password using this link: {full_reset_url}',
                'ssesconf2024@gmail.com',
                [email]
            )

            messages.success(request, "Password reset instructions sent to your email.")
            return redirect('career_app/login')
        except User.DoesNotExist:
            messages.error(request, "No user found with that email address.")
    return render(request, 'career_app/email/forgot_password.html')


# Reset password
def reset_password(request, reset_id):
    reset = get_object_or_404(PasswordReset, reset_id=reset_id, is_used=False)

    if request.method == "POST":
        new_password = request.POST.get('new_password')
        user = reset.user
        user.set_password(new_password)
        user.save()

        reset.is_used = True
        reset.save()

        messages.success(request, "Password reset successfully. Please log in.")
        return redirect('career_app/login')

    return render(request, 'career_app/email/reset_password.html', {'reset_id': reset_id})


# LMS details
def lms_details(request, course_id):
    course = get_object_or_404(LMScourse, id=course_id)
    materials = CourseMaterial.objects.filter(course=course)
    return render(request, 'career_app/course-details.html', {'course': course, 'materials': materials})

# LMS list
def lms(request):
    
    use_external_api = request.GET.get('source') == 'api'

    if use_external_api:
        api_url = settings.CANVAS_API_URL
        token = settings.CANVAS_API_TOKEN
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            courses = response.json()
        else:
            messages.error(request, "Failed to fetch courses from the LMS API.")
            courses = []
    else:
        # Allow all users to view courses, authenticated or not
        courses = LMScourse.objects.all()  # Fetch all courses without filtering by user
        return render(request, "career_app/all-courses.html", {'lms_courses': courses})


 # API endpoint for fetching courses from Canvas
@csrf_exempt
def get_courses(request):
    api_url = settings.CANVAS_API_URL
    token = settings.CANVAS_API_TOKEN
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        return JsonResponse(response.json(), safe=False)
    else:
        return JsonResponse({"error": "Failed to fetch courses"}, status=response.status_code)

# Events view
def events(request):
    return render(request, 'career_app/events.html')

# Event Detail view
def event_detail(request):
    return render(request, 'career_app/event_detail.html')

# Resources view
def resources(request):
    return render(request, 'career_app/resources.html')

def success_view(request):
    return render(request, 'career_app/success.html')  

from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.contrib import messages
from .forms import SubscriptionForm
from .models import Subscriber

def subscribe_view(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # Check if email already exists in the database
            if Subscriber.objects.filter(email=email).exists():
                messages.warning(request, "You are already subscribed!")
            else:
                # Save to database
                subscriber = Subscriber(email=email)
                subscriber.save()

                # Send email notification to admin
                admin_email = "admin@domain.com"
                from_email = "no-reply@domain.com"
                email_subject = "New Newsletter Subscription"
                email_body = f"New subscription from: {email}"
                
                admin_notification = EmailMessage(
                    subject=email_subject,
                    body=email_body,
                    from_email=from_email,
                    to=[admin_email]
                )
                admin_notification.send(fail_silently=False)

                # Send auto-reply to user
                user_subject = "Subscription Confirmed"
                user_body = f"""
                Hello,

                Thank you for subscribing to our newsletter! You'll now receive updates from us.

                Best regards,  
                FCET Omoku Library  
                """
                user_reply = EmailMessage(
                    subject=user_subject,
                    body=user_body,
                    from_email=from_email,
                    to=[email]
                )
                user_reply.send(fail_silently=False)

                messages.success(request, "Thank you for subscribing! A confirmation email has been sent.")

            return redirect('career_app:subscribe')

    else:
        form = SubscriptionForm()
    
    return render(request, "career_app/subscribe.html", {"form": form})
