from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey, DateTimeField, timezone, CharField, TextField


class Queue(models.Model):
    name = CharField(max_length=128)
    description = TextField()

    def __str__(self):
        return str(self.name)

class QueueObject(models.Model):
    user = ForeignKey(User)
    submitted_date = DateTimeField(default=timezone.now)
    description = CharField(max_length=64)

