import datetime
from django.test import TestCase
from user.models import CustomUser
from django.utils import timezone

# Create your tests here.


def create_user_with_access_token(timedelta_hour):
    user = CustomUser()
    user_count = CustomUser.objects.count()
    user.username = 'test_user' + str(user_count)
    user.email = 'test@test'
    user.zoom_access_token = 'testtoken'
    user.zoom_expires_in = timezone.now() + datetime.timedelta(hours=timedelta_hour)
    user.save()
    return user


def create_user_without_access_token():
    user = CustomUser()
    user_count = CustomUser.objects.count()
    user.username = 'test_user' + str(user_count)
    user.email = 'test@test'
    user.save()
    return user


class CustomUserTests(TestCase):

    def test_has_valid_token_valid(self):
        user = create_user_with_access_token(1)
        result = user.has_valid_token()
        self.assertTrue(result)

    def test_has_valid_token_expired(self):
        user = create_user_with_access_token(-1)
        result = user.has_valid_token()
        self.assertFalse(result)

    def test_has_valid_token_empty(self):
        user = create_user_without_access_token()
        result = user.has_valid_token()
        self.assertFalse(result)
