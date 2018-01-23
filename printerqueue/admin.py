from django.contrib import admin

from printerqueue.models import Queue, QueueObject

admin.site.register(Queue)
admin.site.register(QueueObject)

