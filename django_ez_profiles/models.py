import logging

from django.db import models

from django_ez_users.models import CustomUser
# Create your models here.

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Profile(models.Model):

    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="profile", unique=True
    )
    email_comms_opt_in = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)
    current_applications_made = models.IntegerField(
        null=True, blank=True, default=0)
    last_reset = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
