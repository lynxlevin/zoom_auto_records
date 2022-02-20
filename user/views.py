from django.shortcuts import render


def login(request):
    return render(request, 'user/login.html')


def signup(request):
    return render(request, 'user/signup.html')
