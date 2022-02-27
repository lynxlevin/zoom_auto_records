import http
import json
import time
import jwt
import speech_recognition as sr
import environ
from pydub import AudioSegment


def recognize_speech(file_path, language):
    r = sr.Recognizer()
    audio_file = sr.AudioFile(file_path)
    with audio_file as source:
        audio = r.record(source)
    record = r.recognize_google(audio, language=language)
    return record


# TODO: test this method
def convert_m4a_to_flac(file_path, converted_file_path):
    voice = AudioSegment.from_file(file_path, "m4a")
    voice.export(converted_file_path, format="flac")


def access_zoom_api_with_access_token(api, token):
    headers = {
        'authorization': 'Bearer' + token
    }

    response = getresponse_httpsconnection(headers, api)
    data = response.read()
    return json.loads(data)


def access_zoom_api_with_jwt(api):
    token = generate_jwt_token()
    headers = {
        'authorization': 'Bearer' + token,
        'content-type': 'application/json'
    }

    response = getresponse_httpsconnection(headers, api)
    data = response.read()
    return json.loads(data)


def getresponse_httpsconnection(headers, api):
    conn = http.client.HTTPSConnection('api.zoom.us')
    conn.request(api['method'], api['uri'], headers=headers)
    response = conn.getresponse()
    return response


def generate_jwt_token():
    API_KEY = get_secret('ZOOM_API_KEY')
    API_SECRET = get_secret('ZOOM_API_SECRET')

    expiration = int(time.time()) + 5
    payload = {'iss': API_KEY, 'exp': expiration}

    token = jwt.encode(payload, API_SECRET, algorithm='HS256')
    return token


def get_secret(key):
    env = environ.Env()
    env.read_env('.env')
    return env(key)
