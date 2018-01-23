from django.shortcuts import render
from django.contrib.auth.models import User

from .models import Project, ProjectShelf

#TODO View of project, projectshelf and a form to edit and create project

def projectshelf(request):

    return render(request, "projectshelf.html", context={},)
