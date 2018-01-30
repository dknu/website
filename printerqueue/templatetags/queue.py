from django import template
from django.shortcuts import get_object_or_404

from printerqueue.models import Queue

register = template.Library()
from datetime import date


@register.inclusion_tag('printerqueue/queue.html')
def queue_list(can_reserve, qid,  date=date.today()):
    return {
        'can_reserve': can_reserve,
        'qid': qid,
        'intervals':  get_object_or_404(Queue,pk=qid).all_slots(day=date, open_message="Ledig")
            }
