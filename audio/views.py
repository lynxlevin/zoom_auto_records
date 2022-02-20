from email.mime import audio
import jwt
import time
import environ
import json
from django.shortcuts import render
import http.client
import speech_recognition as sr
from pydub import AudioSegment


def input(request):
    return render(request, 'audio/input.html')


def submit(request):
    meeting_id = request.POST['meeting_id']
    meeting = get_zoom_meeting(meeting_id)
    convert_m4a_to_flac()
    record = recognize_speech()
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


def recognize_speech():
    r = sr.Recognizer()
    audio_file = sr.AudioFile('audio/assets/converted.flac')
    with audio_file as source:
        audio = r.record(source)
    record = r.recognize_google(audio)
    return record


def convert_m4a_to_flac():
    # voice = AudioSegment.from_file(
    #     "audio/assets/audio_files_harvard.wav", "wav")
    voice = AudioSegment.from_file("audio/assets/audio_only.m4a", "m4a")
    voice.export("audio/assets/converted.flac", format="flac")
