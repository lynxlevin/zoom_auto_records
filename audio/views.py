from django.http import HttpResponse
from django.shortcuts import render
import http.client


def input(request):
    return render(request, 'audio/input.html')


def submit(request):
    meeting_id = request.POST['meeting_id']
    conn = http.client.HTTPSConnection("api.zoom.us")
    headers = {
        'authorization': "Bearer JWT",
        'content-type': "application/json"
    }
    conn.request("GET", "/v2/meetings/%s" % meeting_id,  headers=headers)
    res = conn.getresponse()
    data = res.read()
    return HttpResponse("Your meeting is %s" % data.decode("utf-8"))
