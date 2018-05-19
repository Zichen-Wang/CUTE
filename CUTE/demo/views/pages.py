from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.template import loader

def index(request):
    template = loader.get_template('demo/index.html')
    return HttpResponse(template.render())
