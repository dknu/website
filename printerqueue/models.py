from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey, DateTimeField, CharField, TextField, IntegerField, BooleanField, \
    FileField


class Queue(models.Model):
    name = CharField(max_length=128)
    description = TextField()
    include_file = BooleanField(default=False)

    def get_objects(self):
        return QueueObject.objects.filter(queue__id=self.id)


    def __str__(self):
        return str(self.name)

class QueueObject(models.Model):
    user = ForeignKey(User)
    submitted_date = DateTimeField()
    description = CharField(max_length=64)
    queue = ForeignKey(Queue)
    file = FileField(null=True)

    start_timedate = DateTimeField(default=None)
    reserved_time = IntegerField()
    end_timedate = DateTimeField(default=None)

    def __str__(self):
        return str(self.user.get_full_name()) + " : " + str(self.start_timedate) + " - " + str(self.end_timedate)
