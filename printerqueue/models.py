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
        self.update()
        reservations = list(self.queueobjects.filter(date=day).order_by('start'))

        open_slots = []

        endobj = QueueObject(
            user=None,
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

                # TODO: New datetime object rounded DOWN to this quarter. If object in interval, set interval start to object
                # TODO: if interval ends before object, exclude interval.

                open_slots.append((prev,obj.start))
            prev = obj.end
        return open_slots

    def all_slots(self, day, open_message="Open"):
        self.update()

        # TODO: Mark or exclude inactive (passed) objects.

        open = list(
            map(
                lambda s: {
                    'start':s[0],
                    'end': s[1],
                    'is_open':True,
                    'message':open_message
                },
                self.get_times_for_day(day)
            )
        )

        reserved = list(
            map(
                lambda o: {
                    'start': o.start,
                    'end': o.end,
                    'is_open': False,
                    'user': o.user,
                    'description': o.description
                },
                self.queueobjects.filter(date=day)
            )
        )

        all = sorted(list(open+reserved), key=lambda s: s['start'])
        for i in range(len(all)):
            all[i]['start'] = str(all[i]['start'])
            all[i]['end'] = str(all[i]['end'])

        return all

    def update(self):

        for queue in list(self.queueobjects.all()):
            queue.update()


    def __str__(self):
        return str(self.name)

class QueueObject(models.Model):
    user = ForeignKey(User, null=True)
    submitted_date = DateTimeField(auto_now=True)
    description = CharField(max_length=64)
    queue = ForeignKey(Queue, related_name='queueobjects')
    file = FileField(null=True)

    date = DateField(default=timezone.now)
    start = TimeField(default=timezone.now)
    end = TimeField(default=timezone.now)

    active = BooleanField(default=True)

    def update(self):

        # Update active-status
        dt_now = timezone.now()
        if (datetime.combine(self.date,self.end) < dt_now):
            self.active = False

    def __str__(self):
        return str(self.user.get_full_name()) + " : " + str(self.date) + "[ " + str(self.start) + " - " + str(self.end) + " ]"
