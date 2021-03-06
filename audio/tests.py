from ast import AnnAssign
import os
import time

from django.urls import reverse
from audio.models import AudioFile
import environ
from unittest.mock import MagicMock, patch
from django.test import TestCase
from audio.domain_logic import access_zoom_api_with_access_token, access_zoom_api_with_jwt, generate_jwt_token, getresponse_httpsconnection, get_secret, recognize_speech
import audio.views as views
from audio.views import access_zoom_api, delete_file, delete_file_and_instance, get_record_from_file
import jwt
from user.tests import create_user_with_access_token, create_user_without_access_token
from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile


def create_audio_file_record():
    file = AudioFile()
    file.file = 'testfile'
    file.save()
    return file


def get_stub_api():
    return {
        'method': 'GET',
        'uri': '/test/',
    }


class AudioViewsPagesTests(TestCase):
    def test_index(self):
        response = self.client.get(reverse('audio:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Zoom会議のミーティングID")

    def test_input(self):
        views.access_zoom_api = MagicMock()
        user = create_user_with_access_token(1)
        self.client.force_login(user)
        meeting_id = '12345'

        response = self.client.post(reverse('audio:input'), {
                                    'meeting_id': meeting_id})

        api = {
            'method': 'GET',
            'uri': '/v2/past_meetings/' + meeting_id + '/instances',
        }
        views.access_zoom_api.assert_called_once_with(
            user, api)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'どのZoom会議？')

    def test_submit(self):
        views.access_zoom_api = MagicMock()
        views.get_record_from_file = MagicMock()
        views.delete_file_and_instance = MagicMock()

        user = create_user_with_access_token(1)
        self.client.force_login(user)

        meeting_uuid = 'test_uuid'
        file = SimpleUploadedFile('test_file.txt', b'this is a test file')

        response = self.client.post(reverse('audio:submit'), {
                                    'meeting_uuid': meeting_uuid, 'file': file})

        api = {
            'method': 'GET',
            'uri': '/v2/past_meetings/' + meeting_uuid,
        }
        views.access_zoom_api.assert_called_once_with(user, api)
        views.get_record_from_file.assert_called_once()
        views.delete_file_and_instance.assert_called_once()


class AudioViewsMethodsTests(TestCase):
    def test_delete_file(self):
        fake_path = 'audio/fake_file.txt'
        open(fake_path, 'w')
        self.assertTrue(os.path.isfile(fake_path))
        delete_file(fake_path)
        self.assertFalse(os.path.isfile(fake_path))

    def test_delete_file_and_instance(self):
        views.delete_file = MagicMock()
        file = create_audio_file_record()
        current_path = os.getcwd()
        audio_file_count = AudioFile.objects.count()

        delete_file_and_instance(file)

        views.delete_file.assert_called_once_with(
            current_path + '/media/testfile')
        self.assertEqual(AudioFile.objects.count(), audio_file_count - 1)

    def test_get_record_from_file(self):
        views.convert_m4a_to_flac = MagicMock()
        views.recognize_speech = MagicMock()
        views.delete_file = MagicMock()
        current_path = os.getcwd()
        file_path = current_path + '/media/testfile'
        converted_file_path = 'audio/tmp/converted.flac'

        file_instance = create_audio_file_record()
        get_record_from_file(file_instance)

        views.convert_m4a_to_flac.assert_called_once_with(
            file_path, converted_file_path)
        views.recognize_speech.assert_called_once_with(
            converted_file_path, 'ja-JP')
        views.delete_file.assert_called_once_with(converted_file_path)

    def test_access_zoom_api_with_access_token(self):
        views.access_zoom_api_with_access_token = MagicMock()
        views.access_zoom_api_with_jwt = MagicMock()
        user = create_user_with_access_token(1)
        api = get_stub_api()

        access_zoom_api(user, api)

        views.access_zoom_api_with_access_token.assert_called_once_with(
            api, 'testtoken')
        views.access_zoom_api_with_jwt.assert_not_called()

    def test_access_zoom_api_without_access_token(self):
        views.access_zoom_api_with_access_token = MagicMock()
        views.access_zoom_api_with_jwt = MagicMock()
        user = create_user_without_access_token()
        api = get_stub_api()

        access_zoom_api(user, api)

        views.access_zoom_api_with_access_token.assert_not_called()
        views.access_zoom_api_with_jwt.assert_called_once_with(api)

    def test_access_zoom_api_with_anonymous_user(self):
        views.access_zoom_api_with_access_token = MagicMock()
        views.access_zoom_api_with_jwt = MagicMock()
        user = AnonymousUser()
        api = get_stub_api()

        access_zoom_api(user, api)

        views.access_zoom_api_with_access_token.assert_not_called()
        views.access_zoom_api_with_jwt.assert_called_once_with(api)


class ExternalLibraryTests(TestCase):
    def test_jwt(self):
        result = jwt.encode({'iss': 'key', 'exp': 5},
                            "secret", algorithm='HS256')
        expected = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJrZXkiLCJleHAiOjV9.jsMSOg4Q5_Lyt49p7qXJNoTSTJa5w4tVX0zPPnkRt8k'
        self.assertEqual(result, expected)


class DomainLogicTests(TestCase):
    @classmethod
    def setUpClass(cls):
        env = environ.Env()
        env.read_env('.env.test')
        super().setUpClass()

    def test_get_secret(self):
        result = get_secret('ZOOM_API_KEY')
        expected = 'test_zoom_api_key'
        self.assertEqual(result, expected)

    def test_generate_jwt_token(self):
        API_KEY = get_secret('ZOOM_API_KEY')
        API_SECRET = get_secret('ZOOM_API_SECRET')
        time.time = MagicMock(return_value=100)
        result = generate_jwt_token()
        expected = jwt.encode(
            {'iss': API_KEY, 'exp': 105}, API_SECRET, algorithm='HS256')
        self.assertEqual(result, expected)

    @patch('http.client.HTTPSConnection.request')
    @patch('http.client.HTTPSConnection.getresponse', return_value='test')
    def test_getresponse_httpsconnection(self, mock_getresponse, mock_request):
        headers = {
            'authorization': 'Bearertoken',
            'content-type': 'application/json'
        }
        api = get_stub_api()

        response = getresponse_httpsconnection(headers, api)

        self.assertEqual(response, 'test')
        mock_getresponse.assert_called_once()
        mock_request.assert_called_once_with(
            api['method'], api['uri'], headers=headers)

    @patch('audio.domain_logic.getresponse_httpsconnection.return_value.read', return_value='{"test": "success"}')
    @patch('audio.domain_logic.getresponse_httpsconnection')
    @patch('audio.domain_logic.generate_jwt_token', return_value='token')
    def test_access_zoom_api_with_jwt(self, mock_jwt, mock_connection, mock_read):
        api = get_stub_api()
        headers = {
            'authorization': 'Bearertoken',
            'content-type': 'application/json'
        }

        result = access_zoom_api_with_jwt(api)
        expected = {"test": "success"}

        self.assertEqual(result, expected)
        mock_jwt.assert_called_once()
        mock_connection.assert_called_once_with(headers, api)
        mock_read.assert_called_once()

    @patch('audio.domain_logic.getresponse_httpsconnection.return_value.read', return_value='{"test": "success"}')
    @patch('audio.domain_logic.getresponse_httpsconnection')
    def test_access_zoom_api_with_access_token(self, mock_connection, mock_read):
        api = get_stub_api()
        token = 'token'
        headers = {
            'authorization': 'Bearer' + token,
        }

        result = access_zoom_api_with_access_token(api, token)
        expected = {"test": "success"}

        self.assertEqual(result, expected)
        mock_connection.assert_called_once_with(headers, api)
        mock_read.assert_called_once()

    @patch('speech_recognition.Recognizer.return_value.recognize_google', return_value='test')
    @patch('speech_recognition.Recognizer.return_value.record', return_value='audio')
    @patch('speech_recognition.AudioFile')
    @patch('speech_recognition.Recognizer')
    def test_recognize_speech(self, mock_sr, mock_audio, mock_record, mock_recognize):
        file_path = '/test_file'
        language = 'ja-JP'
        result = recognize_speech(file_path, language)
        self.assertEqual(result, 'test')
        mock_sr.assert_called_once()
        mock_audio.assert_called_once_with(file_path)
        mock_record.assert_called_once()
        mock_recognize.assert_called_once_with('audio', language=language)
