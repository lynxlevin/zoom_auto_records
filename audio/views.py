import os

from django.http import HttpResponse
from django.shortcuts import render
from audio.forms import AudioFileForm
from audio.models import AudioFile
from audio.domain_logic import recognize_speech, convert_m4a_to_flac, access_zoom_api


def input(request):
    return render(request, 'audio/input.html')


def submit(request):
    form = AudioFileForm(request.POST, request.FILES)
    if form.is_valid():
        file_instance = AudioFile(file=request.FILES['file'])
        file_instance.save()
    else:
        return HttpResponse("fail %s" % form.errors['file'])
    record = get_record_from_file(file_instance)
    delete_uploaded_file_and_instance(file_instance)

    meeting_id = request.POST['meeting_id']
    get_meeting = {
        "method": 'GET',
        "uri": '/v2/meetings/' + meeting_id,
    }
    meeting = access_zoom_api(get_meeting)

    return render(request, 'audio/submit.html', {'uuid': meeting['uuid'], 'topic': meeting['topic'], 'agenda': meeting['agenda'], 'record': record})


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
