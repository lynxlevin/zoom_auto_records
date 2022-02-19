from django.http import HttpResponse
from django.shortcuts import render


def input(request):
    return render(request, 'audio/input.html')
