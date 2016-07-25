from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'base.html', context)

def notimplemented(request):
    return HttpResponse("NXTLVL Method not implemented yet", status=501)

