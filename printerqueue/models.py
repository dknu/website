from datetime import time, timedelta, datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey, DateTimeField, CharField, TextField, IntegerField, BooleanField, \
    FileField, TimeField, DateField
from django.shortcuts import get_object_or_404
from django.utils import timezone


class Queue(models.Model):
    name = CharField(max_length=128)
    description = TextField(default=" No description")
    include_file = BooleanField(default=False)
    include_description = BooleanField(default=True)

    allowed_time_start = TimeField(default=time())
    allowed_time_end = TimeField(default=time())

    hidden = BooleanField(default=False)

    class Meta:
        permissions = (
            ("can_create_queue", "Can create queue"),
        )

    # Finn ledige tidsintervaller for en dag
    def get_times_for_day(self, day):

        reservations = list(self.queueobjects.filter(date=day).order_by('start'))

        open_slots = []

        endobj = QueueObject(
            user=get_object_or_404(User,pk=3),
            queue=self,
            file=None,

            date=day,
            start=self.allowed_time_end,
            end=time(23,59,59)
        )

        reservations.append(endobj)

        prev = self.allowed_time_start
        for obj in reservations:
            td = datetime.combine(day,obj.start) - datetime.combine(day,prev)
            if td.total_seconds() > 0:
                open_slots.append((prev,obj.start))
            prev = obj.end
        return open_slots


    def __str__(self):
        return str(self.name)

class QueueObject(models.Model):
    user = ForeignKey(User)
    submitted_date = DateTimeField(auto_now=True)
    description = CharField(max_length=64)
    queue = ForeignKey(Queue, related_name='queueobjects')
    file = FileField(null=True)

    date = DateField(default=timezone.now)
    start = TimeField(default=timezone.now)
    end = TimeField(default=timezone.now)

    def __str__(self):
        return str(self.user.get_full_name()) + " : " + str(self.date) + "[ " + str(self.start) + " - " + str(self.end) + " ]"
