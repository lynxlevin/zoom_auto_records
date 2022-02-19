from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def input(request):
    return render(request, 'audio/input.html')


def submit(request):
    meeting_id = request.POST['meeting_id']
    return HttpResponseRedirect(reverse('audio:record', args=(meeting_id,)))


def record(request, params):
    return HttpResponse("Your Meeting Id is %s" % params)
