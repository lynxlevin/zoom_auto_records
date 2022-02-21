from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.


class CustomUser(AbstractUser):
    zoom_code = models.CharField(max_length=255, blank=True)
    zoom_access_token = models.CharField(max_length=255, blank=True)
    pass


class CustomUserManager(BaseUserManager):
    pass
