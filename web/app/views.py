# -*- coding: utf-8 -*-
from django.http import JsonResponse, HttpResponse


def hello(request):
    try:
        ret = "hello"
        return HttpResponse(ret)
    except Exception as e:
        raise e