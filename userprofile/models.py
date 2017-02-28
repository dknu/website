import datetime
from calendar import MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY

from django.contrib.auth.admin import User
from django.db import models


class Skill(models.Model):
    title = models.CharField(max_length=30)
    icon = models.ImageField(upload_to="skillicons")

    def __str__(self):
        return self.title


class Group(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class DutyTime(models.Model):
    DUTYDAYS_CHOICES = (
        (MONDAY, 'Mandag'),
        (TUESDAY, 'Tirsdag'),
        (WEDNESDAY, 'Onsdag'),
        (THURSDAY, 'Torsdag'),
        (FRIDAY, 'Fredag')
    )
    t0 = datetime.datetime(year=1, month=1, day=1, hour=12, minute=15)
    t1 = t0 + datetime.timedelta(hours=2)

    day = models.IntegerField(choices=DUTYDAYS_CHOICES, default=MONDAY, blank=False, null=False)
    start_time = models.TimeField(default=t0.time(), blank=False, null=False)
    end_time = models.TimeField(default=t1.time(), blank=False, null=False)

    def __str__(self):
        return '{} {:%H:%M} - {:%H:%M}'.format(self.get_day_display(), self.start_time, self.end_time)


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    image = models.ImageField(upload_to="profilepictures")
    group = models.ManyToManyField(Group, related_name="members")
    access_card = models.CharField(max_length=20, null=True, blank=True)
    skills = models.ManyToManyField(Skill)
    study = models.TextField(null=True, blank=True)
    dutytime = models.ManyToManyField(DutyTime, related_name='profiles')

    def __str__(self):
        return str(self.user)

    @classmethod
    def get_profiles_for_dutytime(cls, day, time):
        return cls.objects.filter(dutytime__day=day, dutytime__start_time__lte=time, dutytime__end_time__gt=time)
