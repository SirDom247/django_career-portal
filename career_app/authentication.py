from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

class EmailVerifiedBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username=username, password=password, **kwargs)
        if user is not None and not user.is_active:
            raise PermissionDenied("Your email is not verified. Please verify your email to log in.")
        return user
