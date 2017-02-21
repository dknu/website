from django.shortcuts import render


def infoscreen(request):
    return render(request, 'infoscreen.html', {})
