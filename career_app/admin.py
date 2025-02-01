from django.contrib import admin
from .models import CustomUser, Contact, LMScourse, CourseMaterial, EmailVerification

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('submitted_at',)


@admin.register(LMScourse)
class LMScourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'start_date', 'end_date', 'created_at', 'instructor_name')
    search_fields = ('title', 'instructor_name')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'material_type', 'file', 'uploaded_at')
    list_filter = ('material_type',)


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "token", "is_verified", "created_at", "expires_at")
    search_fields = ("user__email", "token")
    list_filter = ("is_verified", "created_at", "expires_at")

from .models import Mentor

@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ('user', 'expertise_area', 'created_at', 'updated_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'expertise_area')
    list_filter = ('expertise_area', 'created_at')

from .models import Subscriber

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')  # Show email and date
    search_fields = ('email',)