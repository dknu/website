from django.db import models
from userprofile.models import Profile
from django.utils import timezone


class Project(models.Model):
    project_number = models.IntegerField(unique=True, null=False)
    name = models.CharField(max_length=50, blank=False)
    description = models.TextField()
    owners = models.ManyToManyField(Profile, blank=False)
    contact_phone = models.CharField(max_length=20, blank=False)
    start_date = models.DateTimeField(default=timezone.now)
    last_activated = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)


class ProjectShelf(models.Model):
    MAX_NUMBER_OF_SHELFS = 20
    taken = models.BooleanField(default=False)
    shelf_number = models.IntegerField(unique=True, null=False)
    project_number = models.OneToOneField(Project, on_delete=models.SET_NULL, null=True, blank=True)
    reminder_interval = models.DurationField()

