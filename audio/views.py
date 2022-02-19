import jwt
import time
import environ
import json
from django.http import HttpResponse
from django.shortcuts import render
import http.client


def input(request):
    return render(request, 'audio/input.html')


def submit(request):
    meeting_id = request.POST['meeting_id']
    meeting = get_zoom_meeting(meeting_id)
    return render(request, 'audio/submit.html', {'uuid': meeting['uuid'], 'topic': meeting['topic'], 'agenda': meeting['agenda']})


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
