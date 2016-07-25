from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render

def index(request):
    return HttpResponse('NxtLvl index for Angular APP')

def notimplemented(request):
    return HttpResponse("NXTLVL Method not implemented yet", status=501)

