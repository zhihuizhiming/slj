# -*- coding: utf-8 -*-
from django.http import JsonResponse, HttpResponse
from app.mm.page import get_page, get_img
from utils.logutils import getLogger

Logger = getLogger(False, 'views')

def hello(request):
    try:
        ret = "hello"
        return HttpResponse(ret)
    except Exception as e:
        raise e

def imgs(request, qm):
    try:
        img = get_img(qm)
        return HttpResponse(img, content_type='image/jpg')
    except Exception as e:
        Logger.error("error: %s", e)

def getPage(request, pid):
    try:
        Logger.debug("page id:%s", pid)
        html = get_page(pid)
        Logger.debug("html: %s", html)
        return HttpResponse(html, content_type='text/html')
    except Exception as e:
        raise e

def getPagePic(request, pid, id):
    try:
        Logger.debug("page id:%s, pic id: %s", pid, id)
        html = get_page(pid)
        return HttpResponse(html, content_type='text/html')
    except Exception as e:
        raise e

def test(request):
    test=open('/data/web/static/html/test.html', 'rb').read()
    return HttpResponse(test, content_type='text/html')
