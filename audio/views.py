import os

from django.http import HttpResponse
from django.shortcuts import render
from audio.forms import AudioFileForm
from audio.models import AudioFile
from audio.domain_logic import access_zoom_api_with_access_token, access_zoom_api_with_jwt, recognize_speech, convert_m4a_to_flac


def index(request):
    return render(request, 'audio/index.html')


def input(request):
    meeting_id = request.POST['meeting_id'].replace(' ', '')
    user = request.user

    list_past_meeting_instances = {
        'method': 'GET',
        'uri': '/v2/past_meetings/' + meeting_id + '/instances',
    }
    past_meetings = access_zoom_api(user, list_past_meeting_instances)

    return render(request, 'audio/input.html', {'past_meetings': past_meetings['meetings']})


def submit(request):
    if not 'meeting_uuid' in request.POST:
        return HttpResponse("fail choose a meeting")
    meeting_uuid = request.POST['meeting_uuid']
    user = request.user

    get_past_meeting_details = {
        'method': 'GET',
        'uri': '/v2/past_meetings/' + meeting_uuid,
    }
    meeting = access_zoom_api(user, get_past_meeting_details)

    form = AudioFileForm(request.POST, request.FILES)
    if form.is_valid():
        file_instance = AudioFile(file=request.FILES['file'])
        file_instance.save()
    else:
        return HttpResponse("fail %s" % form.errors['file'])
    record = get_record_from_file(file_instance)
    delete_uploaded_file_and_instance(file_instance)

    context = {
        'uuid': meeting['uuid'],
        'topic': meeting['topic'],
        'start_time': meeting['start_time'],
        'end_time': meeting['end_time'],
        'total_minutes': meeting['total_minutes'],
        'participants_count': meeting['participants_count'],
        'record': record,
    }

    return render(request, 'audio/submit.html', context)


def access_zoom_api(user, api):
    access_token_available = True
    no_access_token = (user.is_anonymous) or (
        user.zoom_access_token == '') or not (access_token_available)
    if no_access_token:
        past_meetings = access_zoom_api_with_jwt(api)
    else:
        access_token = user.zoom_access_token
        past_meetings = access_zoom_api_with_access_token(
            api, access_token)
    return past_meetings


def get_record_from_file(file_instance):
    file_path = file_instance.file.path
    converted_file_path = 'audio/tmp/converted.flac'

    convert_m4a_to_flac(file_path, converted_file_path)
    record = recognize_speech(converted_file_path, 'ja-JP')

    delete_file(converted_file_path)

    return record


def delete_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)


def delete_uploaded_file_and_instance(file_instance):
    path = file_instance.file.path
    delete_file(path)
    file_instance.delete()
