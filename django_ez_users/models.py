import logging

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.dispatch import Signal
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
# Create your models here.

target_reset = Signal()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom User model that uses email instead of username."""

    email = models.EmailField(_("email address"), unique=True)
    email_verified = models.BooleanField(default=False)

    last_verification_email_sent = models.DateTimeField(null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"  # Use email instead of username for authentication
    # These fields will be prompted in createsuperuser
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email


class Profile(models.Model):
    """Profile model for CustomUser."""

    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="profile", unique=True
    )
    email_comms_opt_in = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)
    current_applications_made = models.IntegerField(null=True, blank=True, default=0)
    last_reset = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
