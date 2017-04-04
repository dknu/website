from django.shortcuts import render

from rpi.models import RaspberryPi
from userprofile.models import Profile


def infoscreen(request):
    on_duty = Profile.objects.all()[:2];
    rpis = RaspberryPi.objects.all()
    return render(request, 'infoscreen.html', {
        'on_duty': on_duty,
        'rpis': rpis
    })
