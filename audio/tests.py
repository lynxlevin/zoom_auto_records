import http
import json
import os
import time
import environ
from unittest.mock import MagicMock, Mock, patch
from django.test import TestCase
from audio.domain_logic import access_zoom_api_with_access_token, access_zoom_api_with_jwt, generate_jwt_token, getresponse_httpsconnection, get_secret

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
            'authorization': 'Bearer' + 'token',
            'content-type': 'application/json'
        }
        api = {
            'method': 'GET',
            'uri': '/test/',
        }

        response = getresponse_httpsconnection(headers, api)

        self.assertEqual(response, 'test')
        mock_getresponse.assert_called_once()
        mock_request.assert_called_once_with(
            api['method'], api['uri'], headers=headers)

    @patch('audio.domain_logic.getresponse_httpsconnection.return_value.read', return_value='{"test": "success"}')
    @patch('audio.domain_logic.getresponse_httpsconnection')
    @patch('audio.domain_logic.generate_jwt_token', return_value='token')
    def test_access_zoom_api_with_jwt(self, mock_jwt, mock_connection, mock_read):
        api = {
            'method': 'GET',
            'uri': '/test'
        }
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
        api = {
            'method': 'GET',
            'uri': '/test'
        }
        token = 'token'
        headers = {
            'authorization': 'Bearer' + token,
        }

        result = access_zoom_api_with_access_token(api, token)
        expected = {"test": "success"}

        self.assertEqual(result, expected)
        mock_connection.assert_called_once_with(headers, api)
        mock_read.assert_called_once()
