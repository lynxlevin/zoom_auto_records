import os
from django.test import TestCase

from audio.views import delete_file

# Create your tests here.


class AudioViewsMethodsTests(TestCase):
    def test_delete_file(self):
        fake_path = 'audio/fake_file.txt'
        with open(fake_path, 'w'):
            pass
        delete_file(fake_path)
        self.assertFalse(os.path.isfile(fake_path))
