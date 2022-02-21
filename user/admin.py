from curses.ascii import US
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'zoom_code', 'zoom_access_token', 'is_staff'
    )
    pass


admin.site.register(CustomUser, CustomUserAdmin)
