from django.shortcuts import render
from userprofile.models import Profile


def infoscreen(request):
    on_duty = Profile.objects.all()[:2];
    return render(request, 'infoscreen.html', {'on_duty': on_duty})


