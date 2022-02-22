import base64
import datetime
import json
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from audio.domain_logic import get_secret
import http

from user.forms import SignUpForm


def index(request):
    return render(request, 'user/index.html')


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'user/signup.html'
    success_url = reverse_lazy('audio:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        return HttpResponseRedirect(self.get_success_url())


@login_required
def zoom_init(request):
    uri = "https://zoom.us/oauth/authorize"
    response_type_query = "response_type=code"
    client_id_query = "client_id=" + get_secret('.env', 'ZOOM_CLIENT_ID')
    redirect_uri_query = "redirect_uri=http://localhost:8000/user/zoom/auth/return"

    zoom_auth_url = uri + "?" + response_type_query + \
        "&" + client_id_query + "&" + redirect_uri_query
    return render(request, 'user/zoom_init.html', {'zoom_auth_url': zoom_auth_url})


@login_required
def zoom_return(request):
    if 'code' in request.GET:
        code = request.GET.get('code')
    else:
        code = "couldn't get code"
        return HttpResponse(code)

    user = request.user
    user.zoom_code = code
    user.save()

    data = get_zoom_access_token(code)
    user.zoom_access_token = data['access_token']
    user.zoom_refresh_token = data['refresh_token']
    now = timezone.now()
    user.zoom_expires_in = now + datetime.timedelta(seconds=data['expires_in'])
    user.save()
    return render(request, 'user/zoom_return.html')


def get_zoom_access_token(code):
    client_id = get_secret('.env', 'ZOOM_CLIENT_ID')
    client_secret = get_secret('.env', 'ZOOM_CLIENT_SECRET')
    basic_auth = base64.b64encode(
        (client_id + ":" + client_secret).encode('utf-8'))
    headers = {'authorization': 'Basic' + basic_auth.decode('utf-8')}

    grant_type_query = 'grant_type=authorization_code'
    code_query = 'code=' + code
    redirect_uri_query = "redirect_uri=http://localhost:8000/user/zoom/auth/return"
    uri = '/oauth/token' + '?' + grant_type_query + \
        '&' + code_query + '&' + redirect_uri_query

    conn = http.client.HTTPSConnection('zoom.us')
    conn.request('POST', uri, headers=headers)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data)
