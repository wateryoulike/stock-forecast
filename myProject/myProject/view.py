#oding = utf-8
# -*- coding:utf-8 -*-
from django.http import HttpResponse

def index(request):
    return HttpResponse('Hello World!!!')