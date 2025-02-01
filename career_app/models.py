import uuid
import random
import string
from datetime import timedelta
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

# Utility functions
def generate_random_token():
    return uuid.uuid4().hex

def generate_reset_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=64))

def default_expiration():
    return now() + timedelta(days=1)  # Tokens expire after 24 hours

def get_default_user():
    return User.objects.first().id  # Example: Adjust as needed


# Custom User Manager
class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)

# Custom User Model
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_set", blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email

# Email Verification Model
class EmailVerification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=default_expiration)

    def is_token_valid(self):
        return self.expires_at > now()

    def __str__(self):
        return f"Verification for {self.user.email}"

# Password Reset Model
class PasswordReset(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="password_resets")
    reset_id = models.CharField(max_length=64, unique=True, default=generate_reset_id)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=default_expiration)

    def is_token_valid(self):
        return self.expires_at > now()

    def __str__(self):
        return f"Password reset for {self.user.email}"

# Contact Model
class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

 
class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Mentor Model
class Mentor(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="mentor_profile")
    bio = models.TextField(blank=True, null=True)
    expertise_area = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="mentor_pics/", blank=True, null=True)
    linkedin_url = models.URLField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - Mentor"

    class Meta:
        verbose_name = "Mentor"
        verbose_name_plural = "Mentors"

# Mentor Session Model
class MentorSession(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name="sessions")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="sessions")
    session_date = models.DateTimeField()
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Session with {self.mentor.user.first_name} on {self.session_date}"

    class Meta:
        ordering = ["session_date"]

# LMS Course Model
class LMScourse(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='lms_courses')
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor_name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    materials = models.ManyToManyField('CourseMaterial', related_name="lms_courses_set")

    def __str__(self):
        return self.title

# Course Material Model
class CourseMaterial(models.Model):
    MATERIAL_TYPE_CHOICES = [
        ("video", "Video"),
        ("document", "Document"),
        ("link", "External Link"),
    ]

    course = models.ForeignKey(LMScourse, on_delete=models.CASCADE, related_name="course_materials")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPE_CHOICES)
    file = models.FileField(upload_to="course_materials/", blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

