from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

# Create your models here.


class CustomUser(AbstractUser):
    zoom_code = models.CharField(max_length=255, blank=True)
    zoom_access_token = models.CharField(max_length=255, blank=True)
    zoom_refresh_token = models.CharField(max_length=255, blank=True)
    zoom_expires_in = models.DateTimeField(null=True)
    pass

    def has_valid_token(self):
        empty = self.zoom_access_token == ''
        expired = (not self.zoom_expires_in) or (
            self.zoom_expires_in <= timezone.now())
        return not (empty or expired)


class CustomUserManager(BaseUserManager):
    pass
