from http import HTTPStatus

from django.http.response import HttpResponse


def check_health(request):
    return HttpResponse("ONLINE", status=HTTPStatus.OK)
