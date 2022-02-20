from email.mime import audio
import os

from django.http import HttpResponse
import jwt
import time
import environ
import json
from django.shortcuts import render
import http.client
import speech_recognition as sr
from pydub import AudioSegment
from django.core.files.storage import FileSystemStorage


def input(request):
    return render(request, 'audio/input.html')


def submit(request):
    meeting_id = request.POST['meeting_id']
    meeting = get_zoom_meeting(meeting_id)
    file = request.FILES['file']
    fs = FileSystemStorage()
    filename = fs.save("audio/tmp/%s" % file.name, file)
    convert_m4a_to_flac(filename)
    record = recognize_speech()
    delete_tmp_files(filename)
    return render(request, 'audio/submit.html', {'uuid': meeting['uuid'], 'topic': meeting['topic'], 'agenda': meeting['agenda'], 'record': record})


def get_zoom_meeting(meeting_id):
    token = generate_jwt_token()
    conn = http.client.HTTPSConnection("api.zoom.us")

    headers = {
        'authorization': "Bearer" + token,
        'content-type': "application/json"
    }
    conn.request("GET", "/v2/meetings/%s" % meeting_id,  headers=headers)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data)


def generate_jwt_token():
    env = environ.Env()
    env.read_env('.env')

    API_KEY = env('ZOOM_API_KEY')
    API_SECRET = env('ZOOM_API_SECRET')
    expiration = int(time.time()) + 5
    payload = {'iss': API_KEY, 'exp': expiration}

    token = jwt.encode(payload, API_SECRET, algorithm='HS256')
    return token


def convert_m4a_to_flac(filename):
    voice = AudioSegment.from_file(filename, "m4a")
    voice.export("audio/tmp/converted.flac", format="flac")


def recognize_speech():
    r = sr.Recognizer()
    audio_file = sr.AudioFile('audio/tmp/converted.flac')
    with audio_file as source:
        audio = r.record(source)
    record = r.recognize_google(audio, language='ja-JP')
    return record


def delete_tmp_files(filename):
    converted = 'audio/tmp/converted.flac'
    if os.path.isfile(converted):
        os.remove(converted)
    if os.path.isfile(filename):
        os.remove(filename)
