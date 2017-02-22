from django.shortcuts import render
from userprofile.models import Profile


def infoscreen(request):
    vakter = Profile.objects.all()[:2];
    return render(request, 'infoscreen.html', {'vakter': vakter})
