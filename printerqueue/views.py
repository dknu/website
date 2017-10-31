from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def landing(request):
    context = {"debug":"Debug message"}
    return render(request, 'printerqueue/landing.html', context)
