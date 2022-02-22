import os
from django.test import TestCase
from audio.domain_logic import get_secret

from audio.views import delete_file
import jwt

# Create your tests here.


class AudioViewsMethodsTests(TestCase):
    def test_delete_file(self):
        fake_path = 'audio/fake_file.txt'
        with open(fake_path, 'w'):
            pass
        delete_file(fake_path)
        self.assertFalse(os.path.isfile(fake_path))


class ExternalLibraryTests(TestCase):
    def test_jwt(self):
        result = jwt.encode({'iss': 'key', 'exp': 5},
                            "secret", algorithm='HS256')
        expected = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJrZXkiLCJleHAiOjV9.jsMSOg4Q5_Lyt49p7qXJNoTSTJa5w4tVX0zPPnkRt8k'
        self.assertEqual(result, expected)


class DomainLogicTests(TestCase):
    def test_get_secret(self):
        result = get_secret('.env.test', 'ZOOM_API_KEY')
        expected = 'test_zoom_api_key'
        self.assertEqual(result, expected)
