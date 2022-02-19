from django.http import HttpResponse
from django.shortcuts import render
import http.client


def input(request):
    return render(request, 'audio/input.html')


def submit(request):
    meeting_id = request.POST['meeting_id']
    meeting = get_zoom_meeting(meeting_id)
    return HttpResponse("Your meeting is %s" % meeting)


def get_zoom_meeting(meeting_id):
    conn = http.client.HTTPSConnection("api.zoom.us")
    headers = {
        'authorization': "Bearer JWT",
        'content-type': "application/json"
    }
    conn.request("GET", "/v2/meetings/%s" % meeting_id,  headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")
