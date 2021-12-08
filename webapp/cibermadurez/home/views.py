from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.template import loader

def home(request):
    template = loader.get_template('home/index.html')
    return HttpResponse(template.render({},request))