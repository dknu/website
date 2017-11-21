from django.http import HttpResponse
from django.shortcuts import render

def landing(request):
    context = {"debug":"Debug message"}
    return render(request, 'printerqueue/landing.html', context)

def all_queues(request):
    pass

def create(reques):
    pass

def add_queue(reques):
    pass
