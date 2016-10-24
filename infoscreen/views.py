from django.shortcuts import render


def inforscreen(request):
    return render(request, 'infoscreen.html', {})
