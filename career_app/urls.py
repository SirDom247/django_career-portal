from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import verify_email
from career_app.views import success_view 
from .views import subscribe_view

urlpatterns = [
    # Static Pages
    path('', views.home, name='career_app/home'),
    path('career_app/about/', views.about, name='career_app/aboutus'),
    path('career_app/contact/', views.contact_view, name='career_app/contact'),
    path('career_app/resources/', views.resources, name='career_app/resources'),
    path('career_app/success/', views.success_view, name='career_app/success'),   

    # Authentication
    path('career_app/login/', views.login_view, name='career_app/login'),
    path('career_app/signup/', views.signup, name='career_app/signup'),
    path('career_app/logout/', views.logout_view, name='career_app/logout'),
    path('verify_email/<str:token>/', views.verify_email, name='verify_email'),
    path('career_app/resend-verification-email/<int:user_id>/', views.resend_verification_email, name='career_app/email/resend_verification_email'),
    path('career_app/subscribe/', views.subscribe_view, name='career_app/subscribe'),

    # Password Reset
    path('career_app/password_reset/', auth_views.PasswordResetView.as_view(), name='career_app/password_reset'),
    path('career_app/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='career_app/password_reset_done'),
    path('career_app/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='career_app/password_reset_confirm'),
    path('career_app/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='career_app/password_reset_complete'),
    path('career_app/reset-password/<str:reset_id>/', views.reset_password, name='career_app/reset-password'),
    path('career_app/email/forgot_password/', views.forgot_password, name='career_app/email/forgot-password'),

    # Events
    path('career_app/events/', views.events, name='career_app/events'),
    path('career_app/events/<int:event_id>/', views.event_detail, name='career_app/event_detail'),

    # LMS
    path('career_app/lms/', views.lms, name='career_app/lms'),
    path('career_app/lms/<int:course_id>/', views.lms_details, name='career_app/lms_details'),
    path('career_app/api/get_courses/', views.get_courses, name='career_app/get_courses'),
]
