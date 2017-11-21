from django.contrib import admin

from printerqueue.models import Queue, QueueObject

admin.register(Queue)
admin.register(QueueObject)

