import http
import os
import time
import environ
from unittest.mock import MagicMock, Mock, patch
from django.test import TestCase
from audio.domain_logic import access_zoom_api_with_jwt, generate_jwt_token, get_http_response, get_secret

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

    # def test_get_http_response(self):
    #     mock_connection = Mock(spec=http.client.HTTPSConnection)
    #     mock_connection.getresponse.return_value = 'test'
    #     headers = {
    #         'authorization': 'Bearer' + 'token',
    #         'content-type': 'application/json'
    #     }
    #     api = {
    #         'method': 'GET',
    #         'uri': '/test/',
    #     }
    #     response = get_http_response(headers, api)  # モックが使われていない
    #     self.assertEqual(response, 'test')

    # def mocked_request(*args, **kwargs):
    #     class MockRequest:
    #         def __init__(self):
    #             pass

    #         def request(self, method, uri, headers):
    #             self.response = 'test_response'

    #         def getresponse(self):
    #             return self.response

    #     class MockResponse

    # @patch('audio.domain_logic.generate_jwt_token', return_value='test')
    # def test_access_zoom_api_with_jwt(self, jwt_token_patch):
    #     stub_token = 'test'

    #     # conn = '?'

    #     # stub_headers = {
    #     #     'authorization': 'Bearer' + stub_token,
    #     #     'content-type': 'application/json'
    #     # }
    #     stub_api = {
    #         'method': 'GET',
    #         'uri': '/test'
    #     }

    #     # # conn.request(stub_api['method'], stub_api['uri'], headers=stub_headers)
    #     # # response = conn.getresponse()
    #     # # expected_data = json.loads(response.read())
    #     # result = access_zoom_api_with_jwt(stub_api)
    #     self.assertEqual(access_zoom_api_with_jwt(stub_api), stub_token)
    #     jwt_token_patch.assert_called_once()
