from audioop import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import environ

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
    env = environ.Env()
    env.read_env('.env')

    uri = "https://zoom.us/oauth/authorize"
    response_type_query = "response_type=code"
    client_id_query = "client_id=" + env('ZOOM_CLIENT_ID')
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

    user = request.user
    user.zoom_code = code
    user.save()

    # zoomへ通信、access_tokenを取得
    # codeを削除、access_tokenを保存
    # お帰りなさいページを表示して、audioへのリンクを出す
    # ログインしていないユーザーの場合、zoom/initに入れないようにする？
    return render(request, 'user/zoom_return.html', {'code': code})
