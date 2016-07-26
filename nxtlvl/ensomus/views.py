from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View


def index(request):
    context = {}
    return render(request, 'index.html', context)

def notimplemented(request):
    return HttpResponse("NXTLVL Method not implemented yet", status=501)


class UsersView(View):

    # @login_required
    # @staff_member_required
    # @user_passes_test(lambda u: u.is_superuser) # Probably it should be set of users (manager/superadmin)?
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        return HttpResponse('User: GET {}'.format(user_id))

    def post(self, request, *args, **kwargs):
        return HttpResponse('User: POST')

    def put(self, request, *args, **kwargs):
        return HttpResponse('User: PUT')

    def patch(self, request, *args, **kwargs):
        return HttpResponse('User: PATCH')
