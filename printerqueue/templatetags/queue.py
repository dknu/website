from django import template

register = template.Library()


@register.inclusion_tag('printerqueue/queue.html')
def queue_list(can_reserve, qid, intervals):
    return {
        'can_reserve': can_reserve,
        'qid': qid,
        'intervals': intervals
            }
